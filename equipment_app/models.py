from os import path

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class JobTitleModel(models.Model):
    """ Таблица должностей """

    job_title = models.CharField("Должность", max_length=200)

    class Meta:
        verbose_name = _("должность")
        verbose_name_plural = _("должности")
        managed = False
        db_table = 'ToDo_tasks_jobtitlemodel'

    def __str__(self):
        return f'{self.job_title}'


class CityDepModel(models.Model):
    """Таблица городов"""
    city = models.CharField(verbose_name="Город", max_length=100)
    name_dep = models.CharField(verbose_name="Наименование организации", max_length=350)

    class Meta:
        managed = False
        verbose_name = _("город/организация")
        verbose_name_plural = _("города/организации")
        db_table = 'admin_panel_app_citydepmodel'

    def __str__(self):
        return f'{self.city} - {self.name_dep}'


class GroupDepartmentModel(models.Model):
    """Таблица управлений"""
    group_dep_abr = models.CharField("Сокращенное название управления", max_length=10)
    group_dep_name = models.CharField("Полное название управления", max_length=250)
    city_dep = models.ForeignKey(CityDepModel, verbose_name="Город", on_delete=models.SET_NULL, null=True, blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.group_dep_abr}, {self.group_dep_name}'

    class Meta:
        verbose_name = _("управление")
        verbose_name_plural = _("управления")
        managed = False
        db_table = 'ToDo_tasks_groupdepartmentmodel'


class CommandNumberModel(models.Model):
    """Таблица отделов"""
    command_number = models.IntegerField("Номер отдела/Сокращение")
    command_name = models.CharField("Наименование отдела", max_length=150)
    department = models.ForeignKey(GroupDepartmentModel, verbose_name="Управление", on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.command_number}, {self.command_name}'

    class Meta:
        verbose_name = _("номер отдела")
        verbose_name_plural = _("номера отделов")
        managed = False
        db_table = 'ToDo_tasks_commandnumbermodel'


class EmployeeModel(models.Model):
    """Таблица сотрудников"""
    user = models.OneToOneField(User, models.PROTECT, verbose_name="Пользователь", related_name='phonebook_emp_user')
    last_name = models.CharField("Фамилия", max_length=150)
    first_name = models.CharField("Имя", max_length=150)
    middle_name = models.CharField("Отчество", max_length=150)
    personnel_number = models.CharField("Табельный номер", max_length=20, null=True, default=None)
    job_title = models.ForeignKey(JobTitleModel, on_delete=models.PROTECT, null=True, verbose_name="Должность")
    department = models.ForeignKey(CommandNumberModel, on_delete=models.PROTECT, null=True, verbose_name="№ отдела")
    user_phone = models.IntegerField("№ телефона внутренний", null=True, default=None, blank=True)
    department_group = models.ForeignKey(GroupDepartmentModel, on_delete=models.SET_NULL, default=None, null=True,
                                         verbose_name="Управление")
    right_to_sign = models.BooleanField(verbose_name="Право подписывать задания", default=False)
    check_edit = models.BooleanField("Возможность редактирования задания", default=True)
    can_make_task = models.BooleanField("Возможность выдавать задания", default=True)
    cpe_flag = models.BooleanField("Флаг ГИП (техническая метка)", default=False)
    mailing_list_check = models.BooleanField("Получать рассылку", default=True)
    work_status = models.BooleanField("Сотрудник работает", default=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        managed = False
        verbose_name = _("сотрудник")
        verbose_name_plural = _("сотрудники")
        db_table = 'ToDo_tasks_employee'


def upload_to(instance, filename):
    name_to_path = str(instance.emp.id)
    new_path = path.join('files',
                         # "media", filename)
                         name_to_path,
                         filename)
    print(new_path)
    return new_path


class MoreDetailsEmployeeModel(models.Model):
    """Дополнительная информация по сотрудникам"""
    emp = models.OneToOneField(EmployeeModel, models.CASCADE, verbose_name="Пользователь")
    photo = models.ImageField(verbose_name="Файл", null=True, blank=True,
                              upload_to=upload_to)
    outside_email = models.EmailField(verbose_name="Внешняя почта", null=True, blank=True)
    mobile_phone = models.CharField(verbose_name="Мобильный телефон", null=True, blank=True, max_length=30)
    date_birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    room = models.CharField(verbose_name="Номер комнаты", null=True, blank=True, max_length=30)
    date_birthday_show = models.BooleanField(verbose_name="Отображать день рождения", default=False, null=True)
    city_dep = models.ForeignKey(CityDepModel, on_delete=models.PROTECT, null=True, verbose_name="Город/Подразделение",
                                 blank=True)
    send_email_salary_blank = models.BooleanField(verbose_name="Отсылать расчетный листок", default=False)

    class Meta:
        managed = False
        verbose_name = _("дополнительная информация по сотруднику")
        verbose_name_plural = _("дополнительная информация по сотрудникам")
        db_table = 'admin_panel_app_moredetailsemployeemodel'

    def __str__(self):
        return f'{self.emp}'


class TypeOfEquipmentModel(models.Model):
    """Тип оборудования"""
    equipment_type_name = models.CharField(verbose_name="Тип оборудования", max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _("тип оборудования")
        verbose_name_plural = _("типы оборудования")

    def __str__(self):
        return f'{self.equipment_type_name}'


class TypeOfCoreModel(models.Model):
    """Тип процессора"""
    core_name = models.CharField(verbose_name="Название процессора", max_length=250, null=True, blank=True)
    count_of_core = models.IntegerField(verbose_name="Количество ядер", blank=True, null=True)
    core_frequency = models.IntegerField(verbose_name="Частота процессора", blank=True, null=True)
    core_manufacturer = models.CharField(verbose_name="Производитель", blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = _("процессор")
        verbose_name_plural = _("процессоры")

    def __str__(self):
        return f'{self.core_name} - {self.count_of_core} - {self.core_frequency}'


class TypeOfRAMModel(models.Model):
    """Типы оперативной памяти"""

    ram_type_name = models.CharField(verbose_name="Название памяти", max_length=10, null=True, blank=True)
    ram_manufacturer = models.CharField(verbose_name="Производитель RAM", max_length=100, null=True, blank=True)
    ram_frequency = models.IntegerField(verbose_name="Частота RAM", null=True, blank=True)
    ram_memory_size = models.IntegerField(verbose_name="Объем памяти RAM", null=True, blank=True)
    ram_memory_standard = models.CharField(verbose_name="Стандарт памяти RAM", null=True, blank=True,
                                              help_text="DDR4/DDR5", max_length=10)

    class Meta:
        verbose_name = _("оперативная память")
        verbose_name_plural = _("оперативные памяти")

    def __str__(self):
        return f'{self.ram_type_name}: {self.ram_memory_size}, {self.ram_memory_standard} ({self.ram_frequency})'


class TypeOfVideoCardModel(models.Model):
    """Типы видеокарт"""
    video_card_name = models.CharField(verbose_name="Название видеокарты", max_length=250, null=True, blank=True)
    video_card_memory_size = models.IntegerField(verbose_name="Объем видеопамяти", null=True, blank=True)


    class Meta:
        verbose_name = _("видеокарта")
        verbose_name_plural = _("видеокарты")

    def __str__(self):
        return f'{self.video_card_name} - {self.video_card_memory_size}'


class TypeOfHardDiskModel(models.Model):
    """Типы жестких диcков"""

    class TypeDiskChoice(models.IntegerChoices):
        """Тип жесткого диска"""
        HDD = 1, _('HDD')
        SSD = 2, _('SSD')

    class TypeInterfaceChoice(models.IntegerChoices):
        """Тип жесткого диска"""
        SATA = 1, _('SATA')
        SAS = 2, _('SAS')
        M2 = 3, _('M2')

    type_disk = models.IntegerField(verbose_name="Тип диска", choices=TypeDiskChoice.choices, null=True, blank=True)
    disk_memory_size = models.IntegerField(verbose_name="Размер памяти диска", null=True, blank=True)
    disk_manufacturer = models.CharField(verbose_name="Производитель диска", max_length=100, null=True, blank=True)
    disk_interface = models.IntegerField(verbose_name="Интерфейс диска", choices=TypeInterfaceChoice.choices, null=True, blank=True)

    class Meta:
        verbose_name = _("жесткий диск")
        verbose_name_plural = _("жесткие диски")

    def __str__(self):
        return f'{self.disk_manufacturer}: {self.type_disk} - {self.disk_memory_size} - {self.disk_interface}'


class EquipmentSpecificationsModel(models.Model):
    """Характеристики оборудования"""

    class TypeOfPrintChoice(models.IntegerChoices):
        """Тип печати"""
        JET  = 1, _('Струйный')
        LASER = 2, _('Лазерный')

    class TypeOfPaperChoice(models.IntegerChoices):
        """Тип печати"""
        A4  = 4, _('A4')
        A3  = 3, _('A3')
        A2  = 2, _('A2')
        A1  = 1, _('A1')
        A0  = 0, _('A0')

    equipment_specifications_name = models.CharField(verbose_name="Наименование", max_length=250, null=True, blank=True)
    equipment_type = models.ForeignKey(TypeOfEquipmentModel, verbose_name="Тип оборудования", blank=True, null=True,
                                       on_delete=models.SET_NULL)
    core = models.ForeignKey(TypeOfCoreModel, verbose_name="Процессор", blank=True, null=True,
                             on_delete=models.SET_NULL)
    ram = models.ForeignKey(TypeOfRAMModel, verbose_name="Оперативная память", blank=True, null=True,
                            on_delete=models.SET_NULL)
    video_card = models.ForeignKey(TypeOfVideoCardModel, verbose_name="Видеокарта", blank=True, null=True,
                                   on_delete=models.SET_NULL)
    disk = models.ForeignKey(TypeOfHardDiskModel, verbose_name="Жесткий диск", blank=True, null=True, on_delete=models.SET_NULL)
    diagonal = models.IntegerField(verbose_name="Диагональ", blank=True, null=True)
    description = models.CharField(verbose_name="Примечание", max_length=250, null=True, blank=True)
    type_of_print = models.IntegerField(verbose_name="Тип печати", choices=TypeOfPrintChoice.choices, null=True, blank=True)
    paper_format = models.IntegerField(verbose_name="Тип бумаги", choices=TypeOfPaperChoice.choices, null=True, blank=True)
    count_ethernet_ports = models.IntegerField(verbose_name="Количество портов Ethernet", blank=True, null=True)

    class Meta:
        verbose_name = _("характеристика оборудования")
        verbose_name_plural = _("характеристики оборудования")

    def __str__(self):
        return f'{self.equipment_type}: {self.equipment_specifications_name}'


class EquipmentModel(models.Model):
    """Техника"""
    equipment_name = models.CharField(verbose_name="Наименование", max_length=250, null=True, blank=True)
    equipment_model = models.CharField(verbose_name="Модель", max_length=250, null=True, blank=True)
    equipment_serial_number = models.CharField(verbose_name="Серийный номер", max_length=500, null=True, blank=True)
    equipment_inventory_number = models.CharField(verbose_name="Инвентарный номер", max_length=250, null=True, blank=True)
    equipment_type = models.ForeignKey(TypeOfEquipmentModel, verbose_name="Тип техники", null=True, blank=True, on_delete=models.SET_NULL)
    equipment_spec = models.ForeignKey(EquipmentSpecificationsModel, verbose_name="Характеристики", null=True, blank=True, on_delete=models.SET_NULL)
    barcode = models.CharField(verbose_name="Штрих код", max_length=500, null=True, blank=True)
    description = models.CharField(verbose_name="Примечание", max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _("оборудование")
        verbose_name_plural = _("оборудование")

    def __str__(self):
        return f'{self.equipment_type}: {self.equipment_name}'
#
# class EquipmentEmployeeModel(models.Model):
#     """Техника за сотрудником"""
#
#     equipment = models.OneToOneField(EquipmentModel, verbose_name="Оборудование/техника", null=True, blank=True, on_delete=models.SET_NULL)
#     emp = models.ForeignKey(EmployeeModel, verbose_name="Сотрудник", null=True, blank=True, on_delete=models.SET_NULL)
#     room = models.CharField(verbose_name="кабинет", max_length=10, null=True, blank=True)
#
#     class Meta:
#         verbose_name = _("оборудование у сотрудника")
#         verbose_name_plural = _("оборудование у сотрудников")
#
#     def __str__(self):
#         return f'{self.emp}: {self.equipment}'

