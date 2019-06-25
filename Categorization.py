from decimal import Decimal

class Categorization:
    def categorize(self, name,value):
        newVal="0"
        value = value[:-1]

        if name=="sharp":
            name = "s"
            if value == "in":
                value="0"
            else:
                value="1"
            return name+":"+value + ","

        value = float(value)

        if name == "celsius":
            name="c"
            if value>35:
                value=2
            elif value>26:
                value=1
            else:
                value=0
        elif name == "humidity":
            name = "h"
            if value > 35:
                value = 2
            elif value > 26:
                value = 1
            else:
                value = 0
        elif name == "lux":
            name = "l"
            if value > 450.0:
                value = 2
            elif value > 300:
                value = 1
            else:
                value = 0
        elif name == "gassensor":
            name = "g"
            if value > 150:
                value = 2
            elif value > 90:
                value = 1
            else:
                value = 0
        return name+":" + str(value)+ ","
