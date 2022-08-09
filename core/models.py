from django.db import models
from django.utils.translation import gettext as _
from cloudinary.models import CloudinaryField


class Service(models.Model):
    
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    coverPhoto = models.ImageField(_("Cover Photo"), upload_to='services-rest/')
    icon = models.ImageField(_("Icon"), upload_to='services-rest//')
    averagePrice = models.IntegerField(_("Average Field"))

    # moderation
    isActive = models.BooleanField(_("Is Active"), default=True)
    createdAt = models.DateTimeField(_("Created At"), auto_now_add=True)
    updatedAt = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.title


SERVICE_TYPE_CHOICES = (
    ('hourlyPrice','Hourly Service'),
    ('fixedPrice', 'Fixed Price'),
)   
class SubService(models.Model):

    service = models.ForeignKey("core.Service", verbose_name=_("Service"), related_name='subServices', on_delete=models.CASCADE) 
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    coverPhoto = models.ImageField(_("Cover Photo"), upload_to='services-rest/')
    icon = models.ImageField(_("Icon"), upload_to='services-rest/')
    serviceCharge = models.IntegerField(_("Service Charge"), default=20)
    serviceType = models.CharField(_("Service Type"), max_length=50, choices=SERVICE_TYPE_CHOICES)

    # moderation
    isActive = models.BooleanField(_("Is Active"), default=True)
    createdAt = models.DateTimeField(_("Created At"), auto_now_add=True)
    updatedAt = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("SubService")
        verbose_name_plural = _("SubServices")

    def __str__(self):
        return self.title


TYPE_CHOICES = (
    ('radio','Radio'),
    ('checkbox', 'Checkbox'),
    ('input', 'Input'),
)
class ServiceChoice(models.Model):

    subService = models.ForeignKey("core.SubService", verbose_name=_("Sub Service"), related_name='serviceChoices', on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50)
    type = models.CharField(_("Type"), choices=TYPE_CHOICES, default='radio', max_length=50)

    # moderation
    isActive = models.BooleanField(_("Is Active"), default=True)
    createdAt = models.DateTimeField(_("Created At"), auto_now_add=True)
    updatedAt = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("ServiceChoice")
        verbose_name_plural = _("ServiceChoices")

    def __str__(self):
        return self.title


class ChoiceOption(models.Model):

    choice = models.ForeignKey("core.ServiceChoice", verbose_name=_("Service Choice"), related_name='options', on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50)
    taskerFiltering = models.BooleanField(_("Tasker Filtering"), default=False)

    # moderation
    isActive = models.BooleanField(_("Is Active"), default=True)
    createdAt = models.DateTimeField(_("Created At"), auto_now_add=True)
    updatedAt = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("ChoiceOption")
        verbose_name_plural = _("ChoiceOptions")

    def __str__(self):
        return self.title



class Tasker(models.Model):

    user = models.OneToOneField("authAPI.User", verbose_name=_("User"), on_delete=models.CASCADE)

    address = models.CharField(_("Address"), max_length=50)
    coverPhoto = models.ImageField(_("Cover Photo"), upload_to='services-rest/', blank=True, null=True)
    bio = models.TextField(_("Bio"))
    rating = models.DecimalField(_("Rating"), max_digits=5, decimal_places=2, default=0)
    completedTaskCount = models.IntegerField(_("Completed Tasks"), default=0)

    workCities = models.ManyToManyField("core.City", verbose_name=_("Work Cities"), blank=True)
    portofilos = models.ManyToManyField("core.Portfolio", verbose_name=_("Portofilos"), blank=True)
    certificates = models.ManyToManyField("core.Certificate", verbose_name=_("Certificates"), blank=True)

    isAvailable = models.BooleanField(_("Is Available"), default=True)
    topTasker = models.BooleanField(_("Top Tasker"), default=False)
    supervisor = models.BooleanField(_("Supervisor"), default=False)

    # moderation
    isActive = models.BooleanField(_("Is Active"), default=True)
    createdAt = models.DateTimeField(_("Created At"), auto_now_add=True)
    updatedAt = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Tasker")
        verbose_name_plural = _("Taskers")

    def __str__(self):
        return self.user.first_name


class TaskerSkill(models.Model):

    tasker = models.ForeignKey("core.Tasker", verbose_name=_("Tasker"), related_name='skills', on_delete=models.CASCADE)
    subService = models.ForeignKey("core.SubService", verbose_name=_("Sub Service"), related_name='skills', on_delete=models.CASCADE)
    option = models.ForeignKey("core.ChoiceOption", related_name='skills', verbose_name=_("Option"), on_delete=models.CASCADE)
    priceType = models.CharField(_("Price Type"), max_length=50, choices=SERVICE_TYPE_CHOICES, blank=True)
    price = models.IntegerField(_("Price"))

    class Meta:
        verbose_name = _("TaskerSkill")
        verbose_name_plural = _("TaskerSkills")

    def __str__(self):
        return self.option.title
    

    def save(self, *args, **kwargs):
        self.priceType = self.subService.serviceType
        super(TaskerSkill, self).save(*args, **kwargs)


STATUS_CHOICES = (
    ('new','New'),
    ('accepted', 'Accepted'),
    ('inProgress','In Progress'),
    ('completed','Completed'),
    ('closed','Closed'),
)

class Order(models.Model):

    customer = models.ForeignKey("authAPI.User", verbose_name=_("Customer"), related_name='orders', on_delete=models.CASCADE)
    tasker = models.ForeignKey("core.Tasker", verbose_name=_("Tasker"), related_name='orders', on_delete=models.CASCADE)
    subService = models.ForeignKey("core.SubService", verbose_name=_("SubService"), related_name='orders', on_delete=models.CASCADE)
    options = models.ManyToManyField("core.ChoiceOption", verbose_name=_("Options"))

    startDate = models.DateTimeField(_("Start Date"), auto_now=False, auto_now_add=False)
    address = models.CharField(_("Address"), max_length=50)
    status = models.CharField(_("Stauts"), choices=STATUS_CHOICES, default='new', max_length=50)
    reference = models.CharField(_("Reference"), max_length=50)
    detail = models.TextField(_("Detail"))
    photos = models.ManyToManyField("core.OrderPhoto", verbose_name=_("Photos"), blank=True)

    totalAmount = models.DecimalField(_("Total Amount"), max_digits=5, decimal_places=2, default=0)
    discount = models.DecimalField(_("Discount"), max_digits=5, decimal_places=2, default=0)

    # moderation
    isActive = models.BooleanField(_("Is Active"), default=True)
    createdAt = models.DateTimeField(_("Created At"), auto_now_add=True)
    updatedAt = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.subService.title



class OrderPhoto(models.Model):

    photo = models.ImageField(_("Photo"), upload_to='services-rest/')

    class Meta:
        verbose_name = _("OrderPhoto")
        verbose_name_plural = _("OrderPhotos")
    



class Portfolio(models.Model):

    title = models.CharField(_("Title"), max_length=50)
    photo = models.ImageField(_("Photo"), upload_to='services-rest/')

    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

    def __str__(self):
        return self.title


class Certificate(models.Model):

    title = models.CharField(_("Title"), max_length=50)
    photo = models.ImageField(_("Photo"), upload_to='services-rest/')

    class Meta:
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")

    def __str__(self):
        return self.title


class City(models.Model):

    name = models.CharField(_("Name"), max_length=50)
    isActive = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.name



class Comment(models.Model):

    author = models.ForeignKey("authAPI.User", verbose_name=_("Author"), on_delete=models.CASCADE)
    subService = models.ForeignKey("core.SubService", verbose_name=_("Sub Service"), on_delete=models.SET_NULL, blank=True, null=True)
    tasker = models.ForeignKey("core.Tasker", verbose_name=_("Tasker"), on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(_("Text"))
    rating = models.IntegerField(_("Rating"))

    # moderation
    isActive = models.BooleanField(_("Is Active"), default=True)
    createdAt = models.DateTimeField(_("Created At"), auto_now_add=True)
    updatedAt = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.author.first_name

   

