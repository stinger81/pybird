# ##########################################################################
#
#   Copyright (C) 2022-2023 Michael Dompke (https://github.com/stinger81)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Michael Dompke (https://github.com/stinger81)
#   michael@dompke.dev
#
# ##########################################################################
import os

# requires asciidoctor in linux

replace = {".adoc": ".html"}
files = ["App_Development_Guide.adoc",
         "../README.adoc"]

if not os.path.exists("__temp__"):
    print("Creating Temp Directory")
    os.mkdir("__temp__")

for file in files:
    file = file.strip()
    with open(file, "r") as f:
        content = f.read()
        for k, v in replace.items():
            content = content.replace(k, v)
        temp_name = file.replace("../","")
        with open("__temp__/_temp_" + temp_name, "w") as f:
            f.write(content)

    command = f"asciidoctor __temp__/_temp_{temp_name}"
    os.system(command)
    move_html = f"mv __temp__/_temp_{temp_name.replace('.adoc', '.html')} {file.replace('.adoc', '.html')}"
    os.system(move_html)


