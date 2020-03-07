
import xadmin
from xadmin import views
from .models import VerifyCode,EmailVerifyRecord


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "生鲜商城后台"
    site_footer = "freshshop"
    # menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', "send_time","send_type"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)