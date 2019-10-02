import re
from powerline_shell.runcmd import Command
from ..utils import ThreadedSegment


class Defaults:
    INTERFACE = "en0"
    SHOW_OFFLINE = True


def ifconfig_parser(output):
    pattern = "inet (addr:)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    matches = re.findall(pattern, output)
    if len(matches) == 0:
        return None
    else:
        _, value = matches[0]
        ip = value
    return ip


class PrivateIp:
    def get(self, interface):
        ip = self.strategy_ifconfig(interface, ifconfig_parser)
        return ip if ip else self.strategy_hostname()

    @staticmethod
    def strategy_ifconfig(interface, parser):
        try:
            proc = Command(["ifconfig", interface])

            res = proc.out
            err = proc.err

            return None if err else parser(res)

        except OSError:
            return None

    @staticmethod
    def strategy_hostname():
        try:
            proc = Command(["hostname", "-i"])
            res, err = proc.text
            res = res.decode("utf-8").rstrip()

            return None if err else res

        except OSError:
            return None


class Segment(ThreadedSegment):
    def run(self):
        try:
            interface = self.powerline.segment_conf(
                "private_ip", "interface", Defaults.INTERFACE)

            private_ip = PrivateIp()
            ip = private_ip.get(interface)
            self.ip = ip
            # self.info("this is a message")
        except OSError:
            self.ip = None

    def add_to_powerline(self):
        self.join()
        powerline = self.powerline
        theme = powerline.theme
        show_offline = powerline.segment_conf(
            "private_ip", "show_offline", Defaults.SHOW_OFFLINE)

        if self.ip:
            return powerline.append(" " + self.ip + " ",
                                    theme.PRIVATE_IP_FG, theme.PRIVATE_IP_BG)

        if show_offline:
            powerline.append(
                " Offline ", theme.PRIVATE_IP_FG, theme.PRIVATE_IP_OFFLINE)
