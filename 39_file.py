
from django.db import models
from datetime import datetime


def gregorian_to_shamsi(g_y, g_m, g_d):
    gy = g_y - 1600
    gm = g_m - 1
    gd = g_d - 1

    g_day_no = 365*gy + gy//4 - gy//100 + gy//400
    for i in range(gm):
        g_day_no += [31,28,31,30,31,30,31,31,30,31,30,31][i]
    g_day_no += gd

    j_day_no = g_day_no - 79

    j_np = j_day_no // 12053
    j_day_no %= 12053

    jy = 979 + 33*j_np + 4*(j_day_no//1461)
    j_day_no %= 1461

    if j_day_no >= 366:
        jy += (j_day_no - 366)//365
        j_day_no = (j_day_no - 366)%365

    jm_list = [31,31,31,31,31,31,30,30,30,30,30,29]
    jm = 0
    while jm < 11 and j_day_no >= jm_list[jm]:
        j_day_no -= jm_list[jm]
        jm += 1
    jd = j_day_no + 1

    return jy, jm + 1, jd



class Book(models.Model):
    title=models.CharField(max_length=20)
    text=models.TextField()
    page_number=models.PositiveIntegerField(blank=True,null=True)#فیلد اختیاری
    price=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)#فیلد اختیاری
    author=models.CharField(max_length=10,blank=True,null=True)#فیلد اختیاری
    date_time_created=models.DateTimeField(auto_now_add=True)#فقط یکبار تاریخ توسط خود جنگو ثبت میشه
    date_time_edit=models.DateTimeField(auto_now=True)#هربار عوض میشه


    @property
    def created_at_shamsi(self):
        """
        تاریخ شمسی برای نمایش
        """
        jy, jm, jd = gregorian_to_shamsi(
            self.date_time_created.year,
            self.date_time_created.month,
            self.date_time_created.day
        )
        return f"{jy+1}/{jm:02}/{jd+1:02}"
    
    def __str__(self):
        return self.title


class Person(models.Model):
  
    name=models.CharField(max_length=20)
    family=models.TextField()
    age=models.PositiveIntegerField(blank=True,null=True)#فیلد اختیاری
    mojodi=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)#فیلد اختیاری
    born_time=models.DateTimeField(auto_now_add=True)#فقط یکبار تاریخ توسط خود جنگو ثبت میشه
    alive=models.BooleanField()

    jensiat=(
        ("woman","woman"),
        ("man","man")
    )
    gender=models.CharField(choices=jensiat)


    def __str__(self):
        return self.name






