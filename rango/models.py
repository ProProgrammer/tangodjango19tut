from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    # We defined the slug field that we will use with function slugify to replace whitespace with hyphens
    # Eg - 'how do i create a slug in django' turns into 'how-do-i-create-a-slug-in-django'

    def save(self, *args, **kwargs):
        """
        We override the save method of the Category model so that it calls the slugify method and updates the slug field
        Note that everytime the category name is updated, the slug will also change.
        """
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    """
    Now that the model has been updated, the changes must be propagated to the database.
    However, since data already exists within the database, we need to consider the implications of the change.
    Essentially, for all the existing category names, we want to turn them into slugs (which is performed when the
    record is initially saved!).
    When we update the models via the migration tool, it will add the slug field and provide the option of populating
    the field with a default value.
    Obviously, we want a specific value for each entry - so we will first need to perform the migration (python
    manage.py makemigrations rango and then python manage.py migrate) and then re-run the population script. This is
    because the population script will explicitly call the save method on each entry, triggering the save as we
    implemented above and this update the slug accordingly for each entry

    WHen you run the migrate command, it will provide two options. Select the option to provide a default and enter ''
    Then re-run the population script, which will update the slug fields.
    """

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
