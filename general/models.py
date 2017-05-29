from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# Create your models here.


class UsuarioManager(BaseUserManager):
    """Class required by Django for managing our users from the management
    command.
    """

    def create_user(self, email, name, password=None):
        """Creates a new user with the given detials."""

        # Check that the user provided an email.
        if not email:
            raise ValueError('Users must have an email address.')

        # Create a new user object.
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        # Set the users password. We use this to create a password
        # hash instead of storing it in clear text.
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given detials."""

        # Create a new user with the function we created above.
        user = self.create_user(
            email,
            name,
            password
        )

        # Make this user an admin.
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    """A user profile in our system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    nombre = models.CharField(max_length=60, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    tipo = models.PositiveSmallIntegerField(default=0)
    genero_codigo = models.BooleanField(default=False)
    codigo_gen = models.IntegerField(null=True, blank=True)
    fecha_gen = models.DateField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=128)
    cia = models.ForeignKey('Cia', related_name='cias',
                            null=True, blank=True, on_delete=models.PROTECT)
    tz = models.CharField(max_length=40, blank=True)

    # import pytz
    # import datetime

    # >>> utc =pytz.timezone('UTC')
    # >>>
    # >>> datetime.datetime(2017, 5, 9, 12, 0, tzinfo=utc)
    # datetime.datetime(2017, 5, 9, 12, 0, tzinfo=<UTC>)
    # >>> print(datetime)
    # <module 'datetime' from 'C:\\Users\\josepc\\AppData\\Local\\Programs\\Python\\Python36\\lib\\datetime.py'>
    # >>> fecha1 = datetime.datetime(2017, 5, 9, 12, 0, tzinfo=utc)
    # >>> print(fecha1)
    # 2017-05-09 12:00:00+00:00
    # >>> est = pytz.timezone('US/Eastern')
    # >>> fecha2 = fecha1.astimezone(est)
    # >>> print(fecha1)
    # 2017-05-09 12:00:00+00:00
    # >>> print(fecha2)
    # 2017-05-09 08:00:00-04:00

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = "usuario"

    def get_full_name(self):
        """
        Required function so Django knows what to use as the users full name.
        """

        self.nombre + ' ' + self.apellido

    def get_short_name(self):
        """
        Required function so Django knows what to use as the users short name.
        """

        self.name

    def __str__(self):
        """What to show when we output an object as a string."""

        return self.email


class Pais(models.Model):
    pais_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=False, unique=True)
    codigo = models.CharField(max_length=6, blank=False)

    class Meta:
        db_table = "pais"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    estado_id = models.BigAutoField(primary_key=True)
    pais = models.ForeignKey('Pais', related_name='estados',
                             null=False, blank=False, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150,  blank=False)
    codigo = models.CharField(max_length=6,  blank=False)
    fecha = models.DateTimeField(null=True, blank=True)
    costo = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    activo = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        db_table = "estado"
        ordering = ['nombre']

        unique_together = [
            "pais", "nombre"
        ]

    # class Admin:
    #     list_display = ('estado_id', 'nombre', 'pais')
    #     list_filter = ('pais', 'nombre')
    #     ordering = ('nombre',)
    #     search_fields = ('nombre',)

    # La opción list_display controla que columnas aparecen en la tabla de la lista. Por defecto, la lista de cambios muestra una sola columna que contiene la representación en cadena de caracteres del objeto. Aquí podemos cambiar eso para mostrar el título, el editor y la fecha de publicación.
    # La opción list_filter crea una barra de filtrado del lado derecho de la lista. Estaremos habilitados a filtrar por fecha (que te permite ver sólo los libros publicados la última semana, mes, etc.) y por editor.

    # Puedes indicarle a la interfaz de administración que filtre por cualquier campo, pero las claves foráneas, fechas, booleanos, y campos con un atributo de opciones choices son las que mejor funcionan. Los filtros aparecen cuando tienen al menos 2 valores de dónde elegir.

    # La opción ordering controla el orden en el que los objetos son presentados en la interfaz de administración. Es simplemente una lista de campos con los cuales ordenar el resultado; anteponiendo un signo menos a un campo se obtiene el orden reverso. En este ejemplo, ordenamos por fecha de publicación con los más recientes al principio.
    # Finalmente, la opción search_fields crea un campo que permite buscar texto. En nuestro caso, buscará el texto en el campo título (entonces podrías ingresar Django para mostrar todos los libros con "Django" en el título).

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    ciudad_id = models.BigAutoField(primary_key=True)
    estado = models.ForeignKey(
        'Estado', related_name='ciudades', null=False, blank=False, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150,  blank=False)
    codigo = models.CharField(max_length=6,  blank=False)

    class Meta:
        db_table = "ciudad"
        ordering = ['nombre']
        unique_together = [
            "estado", "nombre"
        ]

    def __str__(self):
        return self.nombre


class Cia(models.Model):
    cia_id = models.BigAutoField(primary_key=True)
    razon_social = models.CharField(
        max_length=250, null=False, blank=False, unique=True)
    rif = models.CharField(max_length=35,  blank=False, unique=True)

    class Meta:
        db_table = "cia"
        ordering = ['razon_social']

    def __str__(self):
        return self.razon_social

