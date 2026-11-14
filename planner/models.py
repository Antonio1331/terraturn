from django.db import models

class FieldParcel(models.Model):
    slug = models.SlugField(unique=True)  # 'sirdaryo', 'yangiyul', 'platte'
    label = models.CharField(max_length=160)
    center_lat = models.FloatField()
    center_lon = models.FloatField()
    default_soil = models.CharField(max_length=32, default="clay_loam")
    default_water = models.CharField(max_length=32, default="deficit")
    default_rotation = models.CharField(max_length=64, default="cotton_wheat_fallow")

    def __str__(self):
        return self.label


class ManagementZone(models.Model):
    parcel = models.ForeignKey(FieldParcel, related_name="zones", on_delete=models.CASCADE)
    zone_code = models.CharField(max_length=16)  # 'MZ-01'
    name = models.CharField(max_length=160)
    coords = models.JSONField()  # [[lat, lon], ...]
    smap = models.FloatField()
    ecostress = models.FloatField()
    srtm = models.FloatField()
    bare_days = models.IntegerField()


class MonthlyClimate(models.Model):
    parcel = models.ForeignKey(FieldParcel, related_name="monthly", on_delete=models.CASCADE)
    month_order = models.PositiveSmallIntegerField()  # 1..12
    month_label = models.CharField(max_length=8)      # 'Jan', 'Feb'...
    gpm = models.FloatField()
    et0 = models.FloatField()
    smap = models.FloatField()
    ndvi = models.FloatField()

    class Meta:
        ordering = ["month_order"]


class CropTrait(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=80)
    water_mm = models.IntegerField()
    root_cm = models.IntegerField()
    n_fix_kg = models.IntegerField()
    frost_c = models.IntegerField()
    notes = models.TextField()