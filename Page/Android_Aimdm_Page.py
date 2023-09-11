import Page as public_pack
from Page.Android_Base_Page import AndroidBasePage


class Android_Aimdm_Page(AndroidBasePage):
    def __init__(self, client, times, name):
        AndroidBasePage.__init__(self, client, times, name)

    aimdm_package = "com.tpos.aimdm"

    msg_header_id = "android.widget.TextView"
    msg_tips_id = "%s:id/tip" % aimdm_package
    msg_confirm_id = "%s:id/confirm" % aimdm_package
    msg_alert_id = "%s:id/root_view" % aimdm_package

    def mdm_msg_alert_show(self, time_out=0):
        return self.wait_alert_appear(self.msg_alert_id, time_out)

    def get_msg_tips_text(self):
        ele = self.get_element_by_id(self.msg_tips_id)
        return self.remove_space(self.get_element_text(ele))

    def get_msg_header_text(self):
        ele = self.get_element_by_id(self.msg_tips_id).child(className=self.msg_header_id)
        return self.remove_space(self.get_element_text(ele))

    def click_msg_confirm_btn(self):
        ele = self.get_element_by_id(self.msg_confirm_id)
        self.click_element(ele)

    def confirm_msg_alert_fade(self, text, timeout=0):
        now_time = self.get_current_time()
        while True:
            if self.wait_alert_fade(self.msg_alert_id, 3):
                break
            else:
                # deal with different alert
                if self.get_msg_tips_text() != self.remove_space(text):
                    break
                ele = self.get_element_by_id(self.msg_confirm_id)
                self.click_element(ele)
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@设备的弹框点击无法消失，请检查一下！！！"
            self.time_sleep(1)

