from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Modello per gli Amministratori
class Administrator(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name="Nome")
    last_name = models.CharField(max_length=255, verbose_name="Cognome")
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=255, verbose_name="Password")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Data di registrazione")

    groups = models.ManyToManyField(Group, related_name='admin_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_permissions')

    def __str__(self):
        return f"{self.username}"

# Modello per gli Utenti (User)
class User(models.Model):
    id = models.AutoField(primary_key=True)
    rfid = models.CharField(max_length=50, unique=True, verbose_name="RFID")
    first_name = models.CharField(max_length=255, verbose_name="Nome")
    last_name = models.CharField(max_length=255, verbose_name="Cognome")

    # Cambia related_name per evitare conflitti
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')

    def __str__(self):
        return f"{self.first_name} {self.last_name} (RFID: {self.rfid})"
