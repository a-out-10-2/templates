#!/opt/local/libexec/gnubin/env python3.5
from html.parser import HTMLParser
import webbrowser


class SPDXLicenseSummoner(HTMLParser):

    def __init__(self):
        self.root_address = "https://spdx.org/licenses/"
        self.table = {}
        self.is_title = True

        # initialize other vars
        self.active_profile_href = None
        self.active_license_href = None
        self.active_title = None
        self.active_key = None

        HTMLParser.__init__(self)

    def reset_active_vars(self):
        self.active_profile_href = None
        self.active_license_href = None
        self.active_title = None
        self.active_key = None

    def submit_active_vars(self):
        print("SUBMIT")
        print("\tkey: \'%s\'" % self.active_key)
        print("\ttitle: \'%s\'" % self.active_title)
        print("\tprofile_href: \'%s\'" % (self.root_address + self.active_profile_href))
        print("\tlicense_href: \'%s\'" % (self.root_address + self.active_license_href))
        print()

        # Submit vars
        self.table[self.active_key] = {'title': self.active_title,
                                       'profile_href': (self.root_address + self.active_profile_href),
                                       'license_href': (self.root_address + self.active_license_href)}

    def extract_license_text(self):

        for key in self.table.keys():
            url = self.table[key]['profile_href']

    def get_files(self):
        #TODO: Finish getfiles()
        pass

    def handle_data(self, data):
        # Full Title

        if data.strip() == '' or data == 'Y' or data == 'License Text':
            pass
        else:
            #print("Data = \'%s\'" % data.strip())

            # tick / tock
            if self.is_title:
                self.active_title = data
                self.is_title = False
            else:
                self.active_key = data
                self.is_title = True


    def handle_starttag(self, tag, attrs):

        if 'tbody' in tag or 'tr' in tag or 'td' in tag:
            return
        elif 'a' in tag:

            #print("tag = \'%s\'" % tag)
            #print("attrs = \'%s\'" % attrs)

            if len(attrs) > 1:
                for attr in attrs:
                    if attr[0] == "href":
                        self.active_profile_href = attr[1].lstrip('./')

            elif len(attrs) == 1:
                for attr in attrs:
                    if attr[0] == "href":
                        self.active_license_href = attr[1].lstrip('./')

                        # and also ...
                        self.submit_active_vars()
                        self.reset_active_vars()



            else:
                #raise Exception("Unexpected attr size")
                pass

            # and also ...
            #self.submit_active_vars()
            #self.reset_active_vars()



    # def handle_startendtag(self, tag, attrs):
    #     print("tag = \'%s\'" % tag)
    #     print("attrs = \'%s\'" % attrs)

    # def handle_endtag(self, tag):
    #     print("tag = \'%s\'" % tag)

    # def handle_charref(self, name):
    #     print("name = \'%s\'" % name)

    # def handle_decl(self, decl):
    #     print("decl = \'%s\'" % decl)

    # def handle_comment(self, data):
    #     print("comment = \'%s\'" % data)

    # def handle_pi(self, data):
    #     print("pi = \'%s\'" % data)

    # def handle_entityref(self, name):
    #     print("entityref = \'%s\'" % name)


class SPDXLicenseHTMLParser(HTMLParser):
    pass

if __name__ == "__main__":
    license_summoner = SPDXLicenseSummoner()

    raw_table = open("raw_license_table.html", 'r')
    raw_table_lines = raw_table.readlines()

    license_summoner.feed("\n".join(raw_table_lines))
    license_summoner.extract_license_text()

    #licenses.get_files()

