from django.db import models
from .utils import gen_ip_from_network


class Idc(models.Model):
    name = models.CharField('机房名称', max_length=100)
    address = models.CharField('机房地址', max_length=200)
    contact_name = models.CharField('联系人姓名', max_length=20)
    contact_phone = models.PositiveIntegerField('联系人电话')

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Network(models.Model):
    usage = models.CharField('用途', max_length=100)
    subnet = models.CharField('子网', max_length=20)
    netmask = models.PositiveSmallIntegerField('网络掩码')
    idc = models.ForeignKey(Idc)
    date = models.DateTimeField('添加时间', auto_now=True)

    class Meta:
        verbose_name = '网络'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        super(Network, self).save(*args, **kwargs)
        print(gen_ip_from_network('%s/%d' % (self.subnet, self.netmask)))
        for address in gen_ip_from_network('%s/%d' % (self.subnet, self.netmask)):
            obj = IpAddress(ip_address=address, network=self)
            obj.save()

    def __unicode__(self):
        return "%s/%d" % (self.subnet, self.netmask)

    __str__ = __unicode__


class IpAddress(models.Model):
    ip_address = models.CharField('IP地址', max_length=20)
    network = models.ForeignKey(Network)
    is_vip = models.BooleanField('是否是vip', default=False)

    class Meta:
        verbose_name = 'IP地址'
        verbose_name_plural = verbose_name
        ordering = ['-ip_address']

    @property
    def is_used(self):
        """used"""
        if self.asset_set.count() == 1:
            return True
        else:
            return False

    def __unicode__(self):
        return self.ip_address

    __str__ = __unicode__


class AssetGroup(models.Model):
    name = models.CharField('资产分组', max_length=50)
    common = models.CharField('分组描述', max_length=200)

    class Meta:
        verbose_name = '资产分组'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Asset(models.Model):
    hostname = models.CharField('主机名', max_length=128, blank=True, null=True)
    asset_type_choices = ((0, '物理机'), (1, '虚拟机'), (2, '交换机'), (3, '路由器'), (4, '其它设备'))
    asset_type = models.PositiveSmallIntegerField('资产类型', choices=asset_type_choices, default=1)
    ip = models.ManyToManyField(IpAddress, verbose_name='IP 地址')
    remote_card_ip = models.CharField('远程管理卡地址', max_length=16, null=True, blank=True)
    group = models.ManyToManyField(AssetGroup, verbose_name='资产分组')

    vendor = models.CharField('制造商', max_length=64, null=True, blank=True)
    sn = models.CharField('Serial number', max_length=128, null=True, blank=True)

    cpu_model = models.CharField('CPU model', max_length=64, null=True, blank=True)
    cpu_cores = models.IntegerField('CPU cores', null=True)
    memory = models.CharField('内存(GB)', max_length=64, null=True, blank=True)
    disk_total = models.CharField('磁盘容量', max_length=1024, null=True, blank=True)
    disk_info = models.CharField('磁盘信息', max_length=1024, null=True, blank=True)

    kernel = models.CharField('内核', max_length=128, null=True, blank=True)
    kernel_version = models.CharField('内核版本', max_length=128, null=True, blank=True)
    os = models.CharField('OS', max_length=128, null=True, blank=True)
    os_version = models.CharField('OS version', max_length=16, null=True, blank=True)
    os_arch = models.CharField('OS arch', max_length=16, blank=True, null=True)

    create_date = models.DateTimeField('添加时间', auto_now=True)
    update_date = models.DateTimeField('更新时间', blank=True, null=True)

    comment = models.TextField('备注', max_length=128, default='', blank=True)

    class Meta:
        verbose_name = '资产'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.hostname

    __str__ = __unicode__
