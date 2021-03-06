import math
from pprint import pprint

from . import config
from . import gui
from . import legs

FEET_PER_METRE = 3.281
DEGREES_PER_RADIAN = 57.296
GRADS_PER_DEGREE = 1.111111111

TEMPLATE = """\
*begin ;put a name for your survey here
{date}
{instrument}
*team "Lord Stormageddon" Pony ;put the surveyors names here 
*team "Doctor Evil" Notes
{units}
{data_format}
{data}
*end ;put the same name here as after begin
"""


class ActualImportDialog(gui.ImportDialog):
    def __init__(self, parent, bootloader):
        gui.ImportDialog.__init__(self, parent)
        self.bootloader = bootloader
        self.config = config.get_config(bootloader)
        self.surveys = legs.get_all_surveys(bootloader)
        print("surveys: ")
        pprint(self.surveys)
        for idx, s in enumerate(self.surveys.values()):
            i = self.survey_list.InsertItem(idx, s['time'].strftime("%Y-%m-%d %Hh%M"))
            self.survey_list.SetItem(i, 1, str(s['station_count']))
            self.survey_list.SetItem(i, 2, str(s['leg_count']))
            print("setting item: ", i, "to: ", s['survey'])
            self.survey_list.SetItemData(i, s['survey'])
        for i in range(len(self.surveys)):
            print("getting item: ", i, "is: ", self.survey_list.GetItemData(i))
        self.survey_list.SortItems(self.sort_list)
        self.survey_list.SetColumnWidth(0, -1)
        self.survey_list.SetColumnWidth(1, -2)
        self.survey_list.SetColumnWidth(2, -2)

    def sort_list(self, item1, item2):
        print("sorting: ", item1, item2)
        return self.surveys[item1]['time'] < self.surveys[item2]['time']

    def get_config(self):
        angle = self.angles.GetSelection()
        units = self.units.GetSelection()
        if angle == 0:
            pass
        else:
            self.config.display_style = angle - 1
        if units == 0:
            pass
        else:
            self.config.length_units = units - 1

    def get_date_string(self, survey):
        return "*date {time:%Y.%m.%d}".format(**survey)

    def get_instrument(self):
        return '*instrument Pony "%s"' % self.bootloader.get_name()

    def get_units(self):
        result = ""
        if self.config.length_units == 0:
            result += "*units length metres"
        else:
            result += "*units length feet"
        if self.config.display_style == 1:
            result += "\n*units compass grads"
            result += "\n*units clino grads"
        elif self.config.display_style == 0:
            result += "\n*units compass degrees"
            result += "\n*units clino degrees"
        else:
            pass  # cartesian
        return result

    def get_data_format(self):
        if self.config.display_style == 2:  # cartesian!
            result = "*data cartesian from to easting northing vertical\n\n"
            result += ";from\tto\teasting\tnorthing\tvertical"
        else:
            result = "*data normal from to tape compass clino\n\n"
            result += ";from\tto\ttape\tcompass\tclino"
        return result

    def get_leg_entry(self, leg):
        frm = leg.frm
        to = leg.to
        if self.config.length_units == 1:  # imperial
            deltas = [x * FEET_PER_METRE for x in leg.delta]
        else:
            deltas = leg.delta[:]
        if self.config.display_style == 2:  # cartesian
            return "{frm}\t{to}\t{delta[0]:.2f}\t{delta[1]:.2f}\t{delta[2]:.2f}\n".format(frm=frm, to=to, delta=deltas)
        compass = math.atan2(deltas[0], deltas[1]) * DEGREES_PER_RADIAN
        if compass < 0:
            compass += 360
        extension = math.hypot(deltas[0], deltas[1])
        clino = math.atan2(deltas[2], extension) * DEGREES_PER_RADIAN
        tape = math.hypot(extension, deltas[2])
        if self.config.display_style == 1:  # grads
            compass *= GRADS_PER_DEGREE
            clino *= GRADS_PER_DEGREE
        return "{frm}\t{to}\t{tape:.2f}\t{compass:.1f}\t{clino:.1f}\n".format(frm=frm, to=to, tape=tape,
                                                                              compass=compass, clino=clino)

    def get_text(self, survey, template):
        text = {
            'date': self.get_date_string(survey),
            'instrument': self.get_instrument(),
            'units': self.get_units(),
            'data_format': self.get_data_format(),
        }
        data = ""
        for leg in survey['legs']:
            data += self.get_leg_entry(leg)
        text['data'] = data
        result = template.format(**text)
        time = survey['time'].strftime("%Y-%m-%d %Hh%M")
        return time, result

    def get_texts(self):
        texts = []
        item = -1
        self.get_config()
        while True:
            item = self.survey_list.GetNextSelected(item)
            if item == -1:
                break
            texts.append(self.get_text(self.surveys[self.survey_list.GetItemData(item)], TEMPLATE))
        return texts
