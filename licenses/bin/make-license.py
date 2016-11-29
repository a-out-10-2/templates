#!/opt/local/libexec/gnubin/env python3.5
from html.parser import HTMLParser
import codecs
import os
import os.path
import io
import shutil
import requests


class ProfileParser(HTMLParser):

    def __init__(self, id):

        self.id = id

        self.PROPERTY_LICENSE_TEXT = "spdx:licenseText"
        self.PROPERTY_LICENSE_HEADER = "spdx:standardLicenseHeader"
        self.PROPERTY_CLASS = "license-text"

        self.active_license = io.StringIO()
        self.active_license_header = io.StringIO()

        self.is_license_section = False
        self.is_license_header_section = False

        HTMLParser.__init__(self)

    def error(self, message):
        pass

    def reset_fc(self):
        self.active_license.seek(0)
        self.active_license_header.seek(0)

    def handle_data(self, data):
        if self.is_license_section is True:
            #print("LICENSE = %s" % str(data))
            #self.active_license.write(data)
            print(data, file=self.active_license)
        elif self.is_license_header_section is True:
            #print("HEADER = %s" % str(data))
            #self.active_license_header.write(data)
            print(data, file=self.active_license_header)

    def handle_starttag(self, tag, attrs):

        if 'div' in tag:
            for attr in attrs:
                if 'property' in attr[0] and self.PROPERTY_LICENSE_TEXT in attr[1]:
                    self.is_license_section = True
                elif 'property' in attr[0] and self.PROPERTY_LICENSE_HEADER in attr[1]:
                    self.is_license_header_section = True

            #print("tag = \'%s\'" % tag)
            #print("attrs(%s) = \'%s\'" % (type(attrs), attrs))

    def __str__(self):
        return "[%s]\n[license]\n%s\n[header]\n%s\n" % (self.id, self.active_license, self.active_license_header)

    #def handle_startendtag(self, tag, attrs):
    #     print("tag = \'%s\'" % tag)
    #     print("attrs = \'%s\'" % attrs)

    def handle_endtag(self, tag):
        if 'div' in tag and self.is_license_section is True:
            self.is_license_section = False
        elif 'div' in tag and self.is_license_header_section is True:
            self.is_license_header_section = False

    def get_license(self):
        return self.active_license

    def get_license_header(self):
        return self.active_license_header

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

    def __str__(self):
        return "active_license_header: %s\nactive_license: %s\n" % (str(self.active_license_header), str(self.active_license))




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
        # print("SUBMIT")
        # print("\tkey: \'%s\'" % self.active_key)
        # print("\ttitle: \'%s\'" % self.active_title)
        # print("\tprofile_href: \'%s\'" % (self.root_address + self.active_profile_href))
        # print("\tlicense_href: \'%s\'" % (self.root_address + self.active_license_href))
        # print()

        # Submit vars
        self.table[self.active_key] = {'title': self.active_title,
                                       'profile_href': (self.root_address + self.active_profile_href),
                                       'license_href': (self.root_address + self.active_license_href)}

    def construct_license_profiles(self):

        counter = 0
        #shortstop = 3
        max = len(self.table.keys())

        for key in self.table.keys():
            print("\r %.1f %s\t[%s]" % ((counter/max) * 100, '%', key), end='')
            url = self.table[key]['profile_href']
            r = requests.get(url)

            profile = ProfileParser(key)
            profile.feed(str(r._content))

            self.table[key]['license_text'] = profile.get_license().getvalue()
            self.table[key]['license_header'] = profile.get_license_header().getvalue()

            counter += 1

            #if counter >= shortstop:
            #    break

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
    def write_files(self):
        for key in self.table.keys():

            # Make the license directory
            os.mkdir(key)

            # Reformat the data.

            self.table[key]['title'] = self.table[key]['title'].split('\n')
            self.table[key]['license_header'] = self.table[key]['license_header'].split('\n')
            self.table[key]['license_text'] = self.table[key]['license_text'].split('\n')

            # self.table[key]['title'] = self.table[key]['title'].split('\\n')
            # self.table[key]['license_header'] = self.table[key]['license_header'].split('\\n')
            # self.table[key]['license_text'] = self.table[key]['license_text'].split('\n')

            # print("title(%s):\n%s\n" % (type(self.table[key]['title']),
            #                             self.table[key]['title']))
            # print("license_header(%s):\n%s\n" % (type(self.table[key]['license_header']),
            #                                      self.table[key]['license_header']))
            # print("license_text(%s):\n%s\n" % (type(self.table[key]['license_text']),
            #                                    self.table[key]['license_text']))
            # self.table[key]['title']
            # self.table[key]['license_header']
            # self.table[key]['license_text']

            # Open the files
            title = codecs.open(os.path.join(key, 'title'), 'w', encoding='utf-8')
            header = codecs.open(os.path.join(key, 'header'), 'w', encoding='utf-8')
            body = codecs.open(os.path.join(key, 'body'), 'w', encoding='utf-8')

            # Write the data
            #title.writelines(self.table[key]['title'])
            #header.writelines(self.table[key]['license_header'])
            #body.writelines(self.table[key]['license_text'])
            for line in self.table[key]['title']:
                print(line, file=title)

            for line in self.table[key]['license_header']:
                print(line, file=header)

            for line in self.table[key]['license_text']:
                print(line, file=body)

            # Close the buffers
            title.close()
            header.close()
            body.close()

if __name__ == "__main__":

    if os.path.isdir('target'):
        shutil.rmtree('target')
    os.mkdir('target')
    os.chdir('target')

    license_summoner = SPDXLicenseSummoner()

    raw_table = open(os.path.join('..', "raw_license_table.html"), 'r')
    raw_table_lines = raw_table.readlines()

    license_summoner.feed("\n".join(raw_table_lines))
    license_summoner.construct_license_profiles()

    # for key in license_summoner.table.keys():
    #     print("key: \'%s\'" % key)
    #     print("\ttitle: \'%s\'" % license_summoner.table[key]['title'])
    #     print("\tprofile_href: \'%s\'" % license_summoner.table[key]['profile_href'])
    #     print("\tlicense_href: \'%s\'" % license_summoner.table[key]['license_href'])
    #     print("\tlicense_text: \'%s\'" % license_summoner.table[key]['license_text'])
    #     print("\tlicense_header: \'%s\'" % license_summoner.table[key]['license_header'])

    license_summoner.write_files()

