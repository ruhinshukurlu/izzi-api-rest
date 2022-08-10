from django.db import models
from cloudinary.models import CloudinaryField


class Service(models.Model):
    
    title = models.CharField("Title", max_length=50)
    description = models.TextField("Description")
    coverPhoto = models.ImageField("Cover Photo", upload_to='services-rest/')
    icon = models.ImageField("Icon", upload_to='services-rest//')
    averagePrice = models.IntegerField("Average Field")

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


SERVICE_TYPE_CHOICES = (
    ('hourlyPrice','Hourly Service'),
    ('fixedPrice', 'Fixed Price'),
)   
class SubService(models.Model):

    service = models.ForeignKey("core.Service", verbose_name="Service", related_name='subServices', on_delete=models.CASCADE) 
    title = models.CharField("Title", max_length=50)
    description = models.TextField("Description")
    coverPhoto = models.ImageField("Cover Photo", upload_to='services-rest/')
    icon = models.ImageField("Icon", upload_to='services-rest/')
    serviceCharge = models.IntegerField("Service Charge", default=20)
    serviceType = models.CharField("Service Type", max_length=50, choices=SERVICE_TYPE_CHOICES)

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "SubService"
        verbose_name_plural = "SubServices"

    def __str__(self):
        return self.title


TYPE_CHOICES = (
    ('radio','Radio'),
    ('checkbox', 'Checkbox'),
    ('input', 'Input'),
)
class ServiceChoice(models.Model):

    subService = models.ForeignKey("core.SubService", verbose_name="Sub Service", related_name='serviceChoices', on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=50)
    type = models.CharField("Type", choices=TYPE_CHOICES, default='radio', max_length=50)

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "ServiceChoice"
        verbose_name_plural = "ServiceChoices"

    def __str__(self):
        return self.title


class ChoiceOption(models.Model):

    choice = models.ForeignKey("core.ServiceChoice", verbose_name="Service Choice", related_name='options', on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=50)
    taskerFiltering = models.BooleanField("Tasker Filtering", default=False)

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "ChoiceOption"
        verbose_name_plural = "ChoiceOptions"

    def __str__(self):
        return self.title



class Tasker(models.Model):

    user = models.OneToOneField("authAPI.User", verbose_name="User", on_delete=models.CASCADE)

    address = models.CharField("Address", max_length=50)
    coverPhoto = models.ImageField("Cover Photo", upload_to='services-rest/', blank=True, null=True)
    bio = models.TextField("Bio")
    rating = models.DecimalField("Rating", max_digits=5, decimal_places=2, default=0)
    completedTaskCount = models.IntegerField("Completed Tasks", default=0)

    workCities = models.ManyToManyField("core.City", verbose_name="Work Cities", blank=True)
    portofilos = models.ManyToManyField("core.Portfolio", verbose_name="Portofilos", blank=True)
    certificates = models.ManyToManyField("core.Certificate", verbose_name="Certificates", blank=True)

    isAvailable = models.BooleanField("Is Available", default=True)
    topTasker = models.BooleanField("Top Tasker", default=False)
    supervisor = models.BooleanField("Supervisor", default=False)

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "Tasker"
        verbose_name_plural = "Taskers"

    def __str__(self):
        return self.user.first_name


class TaskerSkill(models.Model):

    tasker = models.ForeignKey("core.Tasker", verbose_name="Tasker", related_name='skills', on_delete=models.CASCADE)
    subService = models.ForeignKey("core.SubService", verbose_name="Sub Service", related_name='skills', on_delete=models.CASCADE)
    option = models.ForeignKey("core.ChoiceOption", related_name='skills', verbose_name="Option", on_delete=models.CASCADE)
    priceType = models.CharField("Price Type", max_length=50, choices=SERVICE_TYPE_CHOICES, blank=True)
    price = models.IntegerField("Price")

    class Meta:
        verbose_name = "TaskerSkill"
        verbose_name_plural = "TaskerSkills"

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

    customer = models.ForeignKey("authAPI.User", verbose_name="Customer", related_name='orders', on_delete=models.CASCADE)
    tasker = models.ForeignKey("core.Tasker", verbose_name="Tasker", related_name='orders', on_delete=models.CASCADE)
    subService = models.ForeignKey("core.SubService", verbose_name="SubService", related_name='orders', on_delete=models.CASCADE)
    options = models.ManyToManyField("core.ChoiceOption", verbose_name="Options")

    startDate = models.DateTimeField("Start Date", auto_now=False, auto_now_add=False)
    address = models.CharField("Address", max_length=50)
    status = models.CharField("Stauts", choices=STATUS_CHOICES, default='new', max_length=50)
    reference = models.CharField("Reference", max_length=50)
    detail = models.TextField("Detail")
    photos = models.ManyToManyField("core.OrderPhoto", verbose_name="Photos", blank=True)

    totalAmount = models.DecimalField("Total Amount", max_digits=5, decimal_places=2, default=0)
    discount = models.DecimalField("Discount", max_digits=5, decimal_places=2, default=0)

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.subService.title



class OrderPhoto(models.Model):

    photo = models.ImageField("Photo", upload_to='services-rest/')

    class Meta:
        verbose_name = "OrderPhoto"
        verbose_name_plural = "OrderPhotos"
    



class Portfolio(models.Model):

    title = models.CharField("Title", max_length=50)
    photo = models.ImageField("Photo", upload_to='services-rest/')

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title


class Certificate(models.Model):

    title = models.CharField("Title", max_length=50)
    photo = models.ImageField("Photo", upload_to='services-rest/')

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"

    def __str__(self):
        return self.title


class City(models.Model):

    name = models.CharField("Name", max_length=50)
    isActive = models.BooleanField("Is Active", default=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name



class Comment(models.Model):

    author = models.ForeignKey("authAPI.User", verbose_name="Author", on_delete=models.CASCADE)
    subService = models.ForeignKey("core.SubService", verbose_name="Sub Service", on_delete=models.SET_NULL, blank=True, null=True)
    tasker = models.ForeignKey("core.Tasker", verbose_name="Tasker", on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField("Text")
    rating = models.IntegerField("Rating")

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.author.first_name


class Blog(models.Model):

    title = models.CharField("Title", max_length=50)
    author = models.ForeignKey("authAPI.User", verbose_name="User", on_delete=models.CASCADE)
    description = models.TextField("description")
    subBlogs = models.ManyToManyField("core.SubBlog", verbose_name="Sub Blogs")
    coverPhoto = models.ImageField("Cover Photo", upload_to='services-rest/')

    # moderation
    isActive = models.BooleanField("Is Active", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updatedAt = models.DateTimeField("Updated At", auto_now=True)
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title


class SubBlog(models.Model):

    title = models.CharField("Title", max_length=50)
    text = models.TextField("Text")

    class Meta:
        verbose_name = "SubBlog"
        verbose_name_plural = "SubBlogs"

    def __str__(self):
        return self.title
