from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from .validators import real_age


User = get_user_model()


class Tag(models.Model):
    tag = models.CharField('Тег', max_length=20)

    class Meta:
        verbose_name = 'теги'
        verbose_name_plural = 'Тег'
    def __str__(self):
        return self.tag


class Birthday(models.Model):

    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
        )
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    )

    class Meta:
        verbose_name = 'дни рождения'
        verbose_name_plural = 'День рождения'
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})


class Congratulation(models.Model):
    """Модель поздравлений (комментариев)."""

    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        verbose_name='День рождения',
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField('Дата поздрвления', auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор поздравления',
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = 'поздравления'
        verbose_name_plural = 'Поздравление'
        ordering = ('created_at',)
    
    def __str__(self):
        return f'От кого - {self.author} || Кому - {self.birthday}'


