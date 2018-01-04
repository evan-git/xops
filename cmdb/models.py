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
#    is_used = models.BooleanField('是否已使用', default=False)
    is_vip = models.BooleanField('是否是vip', default=False)

    class Meta:
        verbose_name = 'IP地址'
        verbose_name_plural = verbose_name
        ordering = ['-ip_address']

    def is_used(self):
        """used"""
        if self.asset_set.all() == 0:
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
    sn = models.CharField('资产序列号', max_length=100)
    asset_type_choices = ((0, '物理机'), (1, '虚拟机'), (2, '交换机'), (3, '路由器'), (4, '其它设备'))
    asset_type = models.PositiveSmallIntegerField('资产类型', choices=asset_type_choices, default=1)
    ip = models.ForeignKey(IpAddress, verbose_name='IP 地址')
    os = models.CharField('操作系统', max_length=50)
    group = models.ManyToManyField(AssetGroup, verbose_name='资产分组')
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '资产'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sn

    __str__ = __unicode__
