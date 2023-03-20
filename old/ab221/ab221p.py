# -*- coding: utf-8 -*-

AB_DEBUG_BUTTON = False
AB_FORCE_CUSTOM_OS = False
AB_DISABLE_LIBROSA = False
AB_DISABLE_SOUNDFILE = False
AB_DISABLE_SIMPLEAUDIO = False
AB_RESIZABLE_WINDOWS = False
AB_BYPASS_BACKCOM_WARN = False

import os, sys, random, webbrowser
from time import time
from os.path import *
from platform import system
from threading import Thread
from traceback import format_exc
from subprocess import call
from configparser import RawConfigParser

from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

from pydub import AudioSegment
from pydub.playback import play
import numpy as np


# Comment out next line when compiling with AB_DISABLE_LIBROSA
if not AB_DISABLE_LIBROSA: from librosa.onset import *

# Comment out next line when compiling with AB_DISABLE_SOUNDFILE
if not AB_DISABLE_SOUNDFILE: import soundfile as sf

# Comment out next line when compiling with AB_DISABLE_SIMPLEAUDIO
if not AB_DISABLE_SIMPLEAUDIO: import simpleaudio

# Names
abVersion = "AudioButcher v2.2.1-p"
abVersionShort = "2.2.1.00"
abKnownVersions = ["2.1.0", "2.1.1", "2.2.0", "2.2.1.00"]
abDescription = """AudioButcher ver. 2.2.1 (Public Release), December 2022

Brought to you by the AudioButcher Team:
MightInvisible, osdwa, Shriki, vanpassinby, Zach Man
"""
abDiscordLnk = "https://discord.gg/gNHxMmfTy4"
abIconB64 = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADqUExURQAAALy8vLq6up6enr6+vpaWlmlp3L29vaenp7S0tFVV4rW1tbi4uAAA/wQE/by8vbm5ub+/v7e3t6ioqKCgoLGxsbi4wXZ21oaG0jg47IeH0h0d9YCA1AIC/gEB/6+vxKurq6iox1ZW4jMz7gcH/RMT+KWlpQ0N+5qamru7u0xM5lJS47a2tpGRzn5+1XNz2Lu7wKmpxo6Ojmpq2L29vxwc9jQ07TQ07kVF6LGxvgMD/oOD0xAQ+rW1wwsL+7KyxD096goK+39/1KSkyKOjowQE/rKysrCwsK6urmpqzQwM+0ZG6Hh41wAAAJ0U8VQAAABOdFJOU///////////////////////////////////////////////////////////////////////////////////////////////////////AKxN+84AAAAJcEhZcwAADsQAAA7EAZUrDhsAAAeqSURBVHhexZoLQxNHFIVjSo1YBokWSqWk+EQrtVaKFgUUqKCi///v9J57z+zM7s5mH9mQT9idOXNnztlNDEl2B98bMOgIp0+lqohL9AgXLpLSOaOGG9y3gQYxJY2l07khsNkW2mQUBZbVggDdUtDIk++zpn+GQ/zKVvYFS+6B1c4DeBPt0xBEbR2aGz8I2lhakg0thdDU0bkBfw/6NI0CaNk1QtssAOVrxBtztwDozN0CoLNtF4JZ23YhmPXi/C0BNuwugOsP8GMA3SYBbt68yVbMaMRGc27ZjtaGBWAnj/imrZWRwV4TbgG2I6oD1NA6gQa4VZrlAywvL5sQuM19W34S2BRWVthIHD3IzkAhwW3CbiuC/4qH/QQIIN4GNeG2JXDyI6yCO3fucLDE2mBtLX57JqeAxuPx3ZWV0egukFO/pAy0S89lCWBdTsZCS4Ml+MasrnIY2AN579498SbRe+SfhfX1dWmpUYaNZthzYmNDAuBBAxwxfhFoHuBYPeovpL0zNgQJwF7G5uZArOgZg/qNDVbNjK2WCkC7JCzphV+VcgBaJWFJn5QC0Arcv3+fLYMVfbG1tSXbxEMA1FAC/BYIA9aaEbHf2nJuK3UGtrfxuy3+9ylCNu+e7CeTyXg8xopTn4QUAr09CpOJOUxSAfzRitvvAsUsF7t9IOchGUCBt8J+ODHs9wBWSweYTLAN5oq6C/6BsFd2/aTXBa4W28sZ8VDJwyk4B/KzQ7UbXEmgEHgAJIPuH1AMcM5oBwFmCeEePnzoHj16xK6iiZz8/xhXuGfIuxr5g7ijKTpgRnB6/JhSfFKce/LkCSTbFoA1m13At0t0sWOlblAXKMRwZDSSH0C5O6UAdBAoFOAgoNIaTB0Oh0/xXY3bFca7HKnHnDOoduGp4XZlmd0ogC2sSIdiDhuU13D2u/FMgbdCtXiAAgcCpqXHmqAzHe2N8BygYGjPRBvNg1EUsdsGmxqTCkCpEpYJz58/p9YQvHRzrocj0bLs16DurQLoH47gLytwwKAsUEjDmoYpK7AF/Bp/eHThGBbkefHiBWNQaI9+6NL5urF3RgGtqaV5ZRkGUKSLl0OXC2FlNexx343YCQGQofER7bm9Pf1tneFPQTc5KwZomECDe6i1BDNfvmRHMHd7DChNRQsFdlvD6WEBDSCoFulVoM4N/hIotEZXcK9esUt/QXWq9Wg1YL8F+WnBW4DQcMkuziByMigEqXZl1nZMYGbRZGlRUqhOwRc1qy6BaYBdwf9hdX8b2mlCcaFpWG2EXkB7LbCgKZiAaTrPllI9A5fleG0ujU2yALpeCKE61nv9eig/Jhos0m1WjwlsRZ62cBmNDQsDAayS61F2TspsUEDbhnV65kxsDojmeH+pjicEbyzEIl1SNhwRMF/Hc0gpdijHP8D6DJYFpNgjIxge7u9rVxNYkUzRMS4iy6iawabW5tHqfwAaFMvI3P39fbSwce7gQGp9uS0+jI6FA01R/wyKUzg4ONjcZDuG7vDnro43utViIfdVUgIpYYtT3r5ll8hfZ4P9BryJoFQNVw9Qz8D7A9P/BVRrce7wcDw+PBwcUqiFLiXevXuXHpiOzDn0UErCldVdsX6EBEACQrEe1hvUEtigVQkm5vEy9tOWKqErKhTKyIiumkE9R+VAA3Rew+n4VO0cvt2gENHRv01y+1LFoOTpfPgR8gZxahoceoCiBzNnyeBqzIF6EEoBVd6/13Yn0svmODrSmnShc+8JhTZgyQiqCY6OjtgqUTOzFp3voVbk+PhYthURpk+tR2efnJxUryDux8fVwzO5n3j7EwpptKrqfzuGdKe9Dujq6dly6uXYnT4H9XmYSqE6YL8d8QstpRiO5OBQBmVCsRWcmp7MoQy7ZhxfzP8gKpszMnWdMFhM8MFgryUfP9qvUumfu/ZeYhZ/w84toBCgvrqqG4rzwZxKD4OK1hrML4B6R1AW8r3eyN+UcHrqTuHEboH5JChwqttqqzPu01RcOa2lcGuG2J+fpxOcCdpI3U1Teem2MeeAe1NAdDbgf3aGm2pSEWYIUPiqXoMggveOX6WrnweznwHlnD4CldgdUC3RLcB/3JdRp0++TcJZKdPTGQCfAujS3OzZSNBXAKxvNsQ0a8RENxMqxQAX3LfG3GK25de+gQZ2F6WgvUAhwIXCTh3hktX6OoxitgH21i2ch8tLNooBzJ4JcK+bNgJ4DQbs2nUzSSGbUgQgIUajceGj0KXCDgLkbHLHbwk+C6PR58/0F0U8zTpjXTDP7Htvwz6MfRkMvvBeg8v48AUNsLzsr7/sXVys6WmQGNAlAPwlgA4DSXCXtgZ1w2y/2g6Ez4I7gO1AeAhwEQj4GwQDdhRgwMWs0loqZFxdXQ2+wv+q9PxPIwH6+X9IxN92tq8lu6e0T759Y6MBcwjwzWgYYy5noA0aYIYEyS+SW9Dk3vJK7KvmluD2iWdsCzMF6AMGWFgC9cZmQQnM2rYLwax1u5AEdOZuAdDZdgtI4I25v/YEtA0BWibAfYFsdoKmcYD2CfLvbVpBSyFqXuOjQEMQt68rAs2MfO86ItDIU+zPPQFtMkqCwNI5QIOYlAY4o0e4cJEqPQeXaA2nT+H79/8BNeXyRCNnMNMAAAAASUVORK5CYII="

if AB_FORCE_CUSTOM_OS: osname = None
else: osname = system()
if osname=="Windows":
    homepath = os.environ["USERPROFILE"]
    temppath = os.environ["TEMP"]
    pbpadx = 0
    def openf(file): os.startfile(file)
elif osname=="Darwin":
    homepath = os.environ["HOME"]
    temppath = "/tmp"
    pbpadx = 18
    def openf(file): call(("open", file))
elif osname=="Linux":
    homepath = os.environ["HOME"]
    temppath = "/tmp"
    pbpadx = 0
    def openf(file): call(("xdg-open", file))
else: #Custom OS
    homepath = "."
    temppath = "."
    pbpadx = 0
    def openf(file): ...


gplLicense = """
                      GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
                            Preamble
  The GNU General Public License is a free, copyleft license for
software and other kinds of works.
  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.
  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.
  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.
  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.
  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.
  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.
  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.
  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.
  The precise terms and conditions for copying, distribution and
modification follow.
                       TERMS AND CONDITIONS
  0. Definitions.
  "This License" refers to version 3 of the GNU General Public License.
  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.
  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.
  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.
  A "covered work" means either the unmodified Program or a work based
on the Program.
  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.
  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.
  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.
  1. Source Code.
  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.
  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.
  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.
  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.
  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.
  The Corresponding Source for a work in source code form is that
same work.
  2. Basic Permissions.
  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.
  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.
  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.
  3. Protecting Users' Legal Rights From Anti-Circumvention Law.
  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.
  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.
  4. Conveying Verbatim Copies.
  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.
  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.
  5. Conveying Modified Source Versions.
  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:
    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.
    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".
    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.
    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.
  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.
  6. Conveying Non-Source Forms.
  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:
    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.
    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.
    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.
    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.
    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.
  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.
  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.
  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.
  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).
  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.
  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.
  7. Additional Terms.
  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.
  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.
  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:
    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or
    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or
    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or
    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or
    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or
    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.
  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.
  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.
  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.
  8. Termination.
  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).
  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.
  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.
  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.
  9. Acceptance Not Required for Having Copies.
  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.
  10. Automatic Licensing of Downstream Recipients.
  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.
  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.
  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.
  11. Patents.
  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".
  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.
  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.
  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.
  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.
  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.
  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.
  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.
  12. No Surrender of Others' Freedom.
  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.
  13. Use with the GNU Affero General Public License.
  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.
  14. Revised Versions of this License.
  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.
  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.
  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.
  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.
  15. Disclaimer of Warranty.
  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
  16. Limitation of Liability.
  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.
  17. Interpretation of Sections 15 and 16.
  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.
                     END OF TERMS AND CONDITIONS
            How to Apply These Terms to Your New Programs
  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.
  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.
    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
Also add information on how to contact you by electronic and paper mail.
  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:
    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".
  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.
  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>.
"""


def run(target, *args):
    Thread(target=target, args=args, daemon=True).start()

def validPath(path):
    return path!="" and path!=()

def getNoExt(name):
    return basename(splitext(name)[0])

def newFileName():
    if useunixfilename.get()==1: return f"untitled_{int(time())}"
    else: return "untitled"

def defOnsPath(ons2):
    if ons2: return "dir_onsets2"
    else: return "dir_onsets"

def binBool(b):
    try: return int(bool(int(b)))
    except ValueError: return 0

def openFile(file):
    try: openf(file)
    except Exception as e: abError("AudioButcher", f"Can't open file:\n{e}")

def updSecImpAudLen():
    abConfig.set("secimpaudlen")
    updateWindow()

def updIgnOnss(ons1var, ons2var, ons2cb):
    if binBool(ons1var.get())==1:
        ons2var.set(1)
        ons2cb.configure(state="disabled")
    else:
        ons2cb.configure(state="normal")
    abConfig.set("ignoreonss", ons1var.get())
    abConfig.set("ignoreons2", ons2var.get())
    updateWindow()

def sec2ms(sec):
    try:
        ms = str(float(sec)*1000)
        if ms[-2:]==".0": ms=ms[:-2]
        return ms
    except ValueError:
        return sec

def audlen(l):
    l = round(l)
    if secimpaudlen.get()==0:
        return f"{l//60}:{str(l%60).zfill(2)}"
    else:
        return f"{l} sec"

def convOns(_onsets):
    try:
        return sorted([int(o) for o in _onsets])
    except Exception as e:
        abError("Onsets", e)
        return None

def checkVersion(version):
    if version in abKnownVersions or AB_BYPASS_BACKCOM_WARN:
        return True
    else:
        return mb.askyesno("Warning", f"This preset has been created using an unknown version of AudioButcher ({version}), and is likely won't work as intended.\n\nDo you want to continue opening this preset anyway?", icon="warning")

def getExportLength():
    if not generating:
        return sd.askfloat("Export", "Exported audio length (in seconds):", initialvalue=abConfig.get("ste"), parent=window)
    else:
        return None

def cboxSel(cbox, val, max=3):
    try: val=int(val)
    except ValueError: val=None
    if val!=None and 0<=val<=max: cbox.current(val)
    else:
        cbox.configure(state="normal")
        cbox.delete(0, END)
        cbox.insert(0, "<Error>")
        cbox.configure(state="readonly")


def importstate(state):
    global importState
    importState = state
    if importState=="wait":
        progress.configure(mode="indeterminate")
        progress.start()
    else:
        progress.configure(mode="determinate")
        progress.stop()

def updateWindow():
    title = abVersion
    if importState!="none":
        title+=f" - {basename(lastSrcPath)} ({audlen(audio.duration_seconds)})"
    if lastSrcIsRaw: title+=" - Raw Data"
    if onsets!=[]:
        if binBool(abConfig.get("ignoreonss"))==0:
            title+=" - Onsets loaded"
            if onsets2!=[]:
                if binBool(abConfig.get("ignoreons2"))==0: title+=" - Start onsets loaded"
                else: title+=" - Start onsets ignored"
        else: title+=" - Onsets ignored"
    if previewing: title+=" - Previewing"
    window.title(title)

    if previewing: menu_prev.entryconfig(1, state="normal")
    else: menu_prev.entryconfig(1, state="disabled")

def updateSymbols(dum=None):
    mode2sym = ["-", "±", "±", ",", "?"]

    s_Size.config(text=mode2sym[c_methDur.current()])
    s_PL.config(text=mode2sym[c_methPause.current()])
    s_FadeIn.config(text=mode2sym[c_methFdIn.current()])
    s_FadeOut.config(text=mode2sym[c_methFdOut.current()])
    s_crossfade.config(text=mode2sym[c_methCrsfd.current()])
    s_repeat.config(text=mode2sym[c_methrep.current()])
    s_segs.config(text=mode2sym[c_remembertype.current()])

    if c_propfadein.current() == 1:
        l_FadeIn.config(text="Fade-in length (%): ")
    else:
        l_FadeIn.config(text="Fade-in length: ")

    if c_propfadeout.current() == 1:
        l_FadeOut.config(text="Fade-out length (%): ")
    else:
        l_FadeOut.config(text="Fade-out length: ")

    if c_repmode.current() == 1:
        l_repeat.configure(text="Repeat segment for: ")
    else:
        l_repeat.configure(text="Repeat segment ... times: ")

    if c_methrepmsk.current() == 0:
        l_minMaskRepeat.config(text="Minimum: ")
        l_maxMaskRepeat.config(text="Maximum: ")
    elif c_methrepmsk.current() in (1, 2):
        l_minMaskRepeat.config(text="Average: ")
        l_maxMaskRepeat.config(text="Deviation: ")
    elif c_methrepmsk.current() == 3:
        l_minMaskRepeat.config(text="Mu (µ): ")
        l_maxMaskRepeat.config(text="Sigma (σ): ")

    if c_propfadeout.current() == 0:
        c_notepropfd.config(state="disabled")
        x_notepropfd.set(0)
    else:
        c_notepropfd.config(state="normal")

    if x_fromseed.get() == 0:
        e_seed.configure(state="disabled")
    else:
        e_seed.configure(state="normal")

    if c_quantizeMode.current() == 0:
        e_quanavgstrt.configure(state="disabled")
        e_quanstrt.configure(state="disabled")
        e_quanseglgth.configure(state="disabled")
        e_quanrep.configure(state="disabled")
        e_quanmask.configure(state="disabled")
        e_bpm.configure(state="disabled")
    else:
        e_quanavgstrt.configure(state="normal")
        e_quanstrt.configure(state="normal")
        e_quanseglgth.configure(state="normal")
        e_quanrep.configure(state="normal")
        e_quanmask.configure(state="normal")
        if c_quantizeMode.current() == 2:
            e_bpm.configure(state="normal")
        else:
            e_bpm.configure(state="disabled")

    if c_quantizeMode.current() == 1:
        e_usestartonsets.configure(state="normal")
    else:
        e_usestartonsets.configure(state="disabled")
    

    if x_trimfile.get() == 0:
        e_trimmin.configure(state="disabled")
        e_trimmax.configure(state="disabled")
        c_shiftons.configure(state="disabled")
    else:
        e_trimmin.configure(state="normal")
        e_trimmax.configure(state="normal")
        c_shiftons.configure(state="normal")

def applyWindowStyle(obj):
    obj.resizable(AB_RESIZABLE_WINDOWS, AB_RESIZABLE_WINDOWS)
    obj.iconphoto(True, PhotoImage(data=abIconB64))

def loadAudio(path):
    try:
        return AudioSegment.from_file(path)
    except Exception:
        if AB_DISABLE_SOUNDFILE: raise
        else:
            y, sr = sf.read(path)
            wavpath = join(temppath, f"ab_convert_{int(time())}.wav")
            sf.write(wavpath, y, sr)
            audio = AudioSegment.from_wav(wavpath)
            try: os.remove(wavpath)
            except Exception: print("Exception caught: loadAudio")
            return audio

def apply210CompMethod(CompMethod):
    if CompMethod=="0":
        e_fdmode_lc.delete(0, END)
        e_fdmode_lc.insert(0, "1")
    elif CompMethod=="1":
        e_fdmode_sf.delete(0, END)
        e_fdmode_sf.insert(0, "1")
    elif CompMethod=="2":
        e_fdmode_en.delete(0, END)
        e_fdmode_en.insert(0, "1")


def speedChange(sound, speed=0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * (2**(speed/12)))})
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def findNearest(array, value, mode, direction = 0):
    #mode 0 returns timestamp, mode 1 returns array index
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()

    if direction == 1:
        if array[idx] > value and idx > 0:
            idx -= 1
    if direction == 2:
        if array[idx] < value and idx < array.size - 1:
            idx += 1

    if mode == 0: return array[idx]
    else: return idx

def generateOnsets(source):
    y = np.array(source.set_frame_rate(22050).set_channels(1).get_array_of_samples()).astype(np.float32)
    sr = 22050
    onset_function = onset_strength(y=y, sr=sr, aggregate=np.median, n_fft=1024, fmax=1500)
    backtrack_function = onset_strength(y=y, sr=sr)
    onset_times = onset_detect(y=y, sr=sr, onset_envelope = onset_function, backtrack=1, energy=backtrack_function, units="time")
    return [round(element * 1000) for element in onset_times]

def processOnsets(mode, _onsets, ons2=False, source=None, parent=None):
    global onsets, onsets2
    if _onsets!=None:
        if mode in [0, 1]:
            try:
                initialfile = getNoExt(source)+" [onsets]"
                selfile = fd.asksaveasfilename(filetypes=onset_types, defaultextension=onset_types, initialdir=abConfig.get("dir_onsets"), initialfile=initialfile, parent=parent)
                if validPath(selfile):
                    abConfig.set("dir_onsets", path=selfile)
                    abofile = open(selfile, "w")
                    for onset in _onsets: abofile.write("%s " % onset)
                    abofile.close()
            except Exception as e:
                abError("Onsets", e)
        if mode in [0, 2]:
            if not ons2: onsets = sorted(_onsets)
            else: onsets2 = sorted(_onsets)
    updateWindow()

def openOnsets(parent, ons2=False):
    selfile = fd.askopenfilename(filetypes=onset_types, initialdir=abConfig.get(defOnsPath(ons2)), parent=parent)
    if validPath(selfile):
        try:
            abConfig.set(defOnsPath(ons2), path=selfile)
            abofile = open(selfile, "r")
            processOnsets(2, convOns(abofile.read().split()), ons2)
            abofile.close()
        except Exception as e:
            abError("Onsets", e)
        else:
            updateWindow()
            mb.showinfo("Onsets", "Applied successfully")
            if closeonsets.get()==1: parent.destroy()

def getOnsets(parent, mode, ons2=False, fromCurrent=False, source=None, window=True):
    global audio
    if fromCurrent:
        source = lastSrcPath
    elif source==None:
        source = fd.askopenfilename(filetypes=import_types, initialdir=abConfig.get("dir_srcaud"), parent=parent)
    if validPath(source):
        try:
            if window: parent.title("Manage onsets - Busy")
            if fromCurrent: _onsets = generateOnsets(audio)
            else: _onsets = generateOnsets(loadAudio(source))
            if window: parent.title("Manage onsets - Ready")
            mb.showinfo("Onsets", "All onsets detected.")
            processOnsets(mode, _onsets, ons2, source, parent)
        except Exception as e:
            if window: parent.title("Onsets - Ready")
            abError("Onsets", e)
        else:
            if closeonsets.get()==1 and window: parent.destroy()

def eoImportOnsets(parent, entry, ons2):
    selfile = fd.askopenfilename(filetypes=onset_types, initialdir=abConfig.get(defOnsPath(ons2)), parent=parent)
    if validPath(selfile):
        try:
            entry.delete("1.0", END)
            abConfig.set("dir_onsets", path=selfile)
            abofile = open(selfile, "r")
            entry.insert(END, abofile.read())
            abofile.close()
        except Exception as e:
            abError("Onsets", e)

def eoCurrentOnsets(entry, ons2):
    global onsets, onsets2
    if not ons2: _onsets = onsets
    else: _onsets = onsets2
    try:
        entry.delete("1.0", END)
        for o in _onsets: entry.insert(END, "%s " % o)
    except Exception as e:
        abError("Onsets", e)


class abConfigure:
    def __init__(self, file, section):
        self.config = RawConfigParser()
        self.file = file
        self.section = section
    def get(self, what):
        try: self.config.read(self.file, encoding="utf-8")
        except Exception:
            print("Exception caught: abConfigure")
        fallbacks = {
            "dir_srcaud":       homepath,
            "dir_resaud":       homepath,
            "dir_presets":      homepath,
            "dir_onsets":       homepath,
            "dir_onsets2":      homepath,
            "lastdebcom":       "...",
            "raw_def_sw":       1,
            "raw_def_cs":       2,
            "raw_def_fr":       44100,
            "ste":              120,
            "stp":              10,
            "useunixfilename":  1,
            "secimpaudlen":     0,
            "shadderrinf":      0,
            "autoonsdet":       0,
            "resetonsets":      1,
            "closeonsets":      0,
            "onsetsdropdown":   2,
            "ignoreonss":       0,
            "ignoreons2":       0,
        }
        if not self.config.has_section(self.section): self.config[self.section] = {}
        return self.config.get(self.section, what, fallback=fallbacks[what])
    def set(self, what, value=0, path=""):
        values = {
            "dir_srcaud":       dirname(path),
            "dir_resaud":       dirname(path),
            "dir_presets":      dirname(path),
            "dir_onsets":       dirname(path),
            "dir_onsets2":      dirname(path),
            "lastdebcom":       value,
            "raw_def_sw":       value,
            "raw_def_cs":       value,
            "raw_def_fr":       value,
            "ste":              value,
            "stp":              stp.get(),
            "useunixfilename":  useunixfilename.get(),
            "secimpaudlen":     secimpaudlen.get(),
            "shadderrinf":      shadderrinf.get(),
            "autoonsdet":       autoonsdet.get(),
            "resetonsets":      resetonsets.get(),
            "closeonsets":      closeonsets.get(),
            "onsetsdropdown":   value,
            "ignoreonss":       value,
            "ignoreons2":       value,
        }
        self.config[self.section][what] = str(values[what])
        cfgfile = open(self.file, "w", encoding="utf-8")
        self.config.write(cfgfile)
        cfgfile.close()

def abDefaultConfig():
    cfgEmpty()
    cfgDefault()
    updateSymbols()

def abJoinDiscord():
    webbrowser.open(abDiscordLnk)

def abShowLicense():
    licwin = Toplevel(window)
    licwin.title("License")
    licwin.geometry("640x480")

    lictext = ScrolledText(licwin, wrap=WORD)
    lictext.insert(END, gplLicense)
    lictext.configure(state=DISABLED)
    lictext.pack(expand=1, fill="both")

    applyWindowStyle(licwin)
    licwin.grab_set()

def abAbout():
    mb.showinfo(abVersion, abDescription)

def abDebug(result):
    com = sd.askstring("Debug", "Execute python command:", initialvalue=abConfig.get("lastdebcom"), parent=window)
    if com!=None:
        abConfig.set("lastdebcom", com)
        try:
            if result: r = eval(com)
            else: exec(com)
        except Exception as e:
            abError("Debug", e)
        else:
            if result: mb.showinfo(com, str(r))

def abOnsetsWindow():
    onswin = Toplevel(window)
    onswin.title("Manage onsets - Ready")
    face = Frame(onswin, padding=3)
    face.pack(expand=1, fill="both")
    group = Frame(face); group.grid(row=0, column=0, columnspan=3, sticky="w")

    x_ignoreonss = IntVar()
    x_ignoreons2 = IntVar()
    x_ignoreonss.set(binBool(abConfig.get("ignoreonss")))
    x_ignoreons2.set(binBool(abConfig.get("ignoreons2")))

    Separator(group, orient=VERTICAL).grid(row=0, column=1, rowspan=2, padx=3, ipady=20)

    b_ons1_file = Button(group, text="Apply onset list from file", command=lambda: openOnsets(onswin))
    b_ons2_file = Button(group, text="Apply start onset list from file", command=lambda: openOnsets(onswin, ons2=True))
    b_ons1_edit = Button(group, text="Manually edit onsets", command=lambda: abEditOnsets(onswin))
    b_ons2_edit = Button(group, text="Manually edit start onsets", command=lambda: abEditOnsets(onswin, ons2=True))
    b_geno_curr = Button(face,  text="Generate onset list from current audio", command=lambda: run(getOnsets, onswin, c_andthen.current(), False, True))
    b_geno_oaud = Button(face,  text="Generate onset list from other file", command=lambda: run(getOnsets, onswin, c_andthen.current()))
    l_andthen = Label(face, text="And then,")
    c_andthen = Combobox(face, values=("Save to file and apply", "Save to file only", "Apply only"), width=20, state="readonly")
    c_ignoreonss = Checkbutton(face, text="Ignore onsets for now", variable=x_ignoreonss, command=lambda: updIgnOnss(x_ignoreonss, x_ignoreons2, c_ignoreons2))
    c_ignoreons2 = Checkbutton(face, text="Ignore start onsets for now", variable=x_ignoreons2, command=lambda: updIgnOnss(x_ignoreonss, x_ignoreons2, c_ignoreons2))

    b_ons1_file.grid(row=0, column=0, sticky="w")
    b_ons2_file.grid(row=0, column=3, sticky="w")
    b_ons1_edit.grid(row=1, column=0, sticky="w")
    b_ons2_edit.grid(row=1, column=3, sticky="w")
    b_geno_curr.grid(row=2, column=0, sticky="w")
    b_geno_oaud.grid(row=3, column=0, sticky="w")
    l_andthen.grid(row=2, column=1, rowspan=2, padx=2)
    c_andthen.grid(row=2, column=2, rowspan=2)
    c_ignoreonss.grid(row=4, column=0, columnspan=2, sticky="w")
    c_ignoreons2.grid(row=5, column=0, columnspan=2, sticky="w")

    if lastSrcPath=="":
        b_geno_curr.configure(state="disabled")

    if AB_DISABLE_LIBROSA:
        b_geno_curr.configure(state="disabled")
        b_geno_oaud.configure(state="disabled")

    c_andthen.bind("<<ComboboxSelected>>", lambda event: abConfig.set("onsetsdropdown", c_andthen.current()))
    cboxSel(c_andthen, abConfig.get("onsetsdropdown"), 2)
    updIgnOnss(x_ignoreonss, x_ignoreons2, c_ignoreons2)

    applyWindowStyle(onswin)
    onswin.grab_set()

def abEditOnsets(parent, ons2=False):
    parent.destroy()
    edonsw = Toplevel(window)
    if not ons2: edonsw.title("Edit onsets")
    else: edonsw.title("Edit start onsets")

    menu_upper = Menu(edonsw, tearoff=False)
    menu_import = Menu(menu_upper, tearoff=False)
    menu_upper.add_cascade(label="Import", menu=menu_import)
    menu_import.add_command(label="Open onsets file", command=lambda: eoImportOnsets(edonsw, t_onsets, ons2))
    menu_import.add_command(label="Import current onsets", command=lambda: eoCurrentOnsets(t_onsets, ons2))
    if ons2: menu_import.add_command(label="Import current usual onsets", command=lambda: eoCurrentOnsets(t_onsets, False))

    menu_lower = Frame(edonsw, padding=1)
    b_apply = Button(menu_lower, text="Apply", command=lambda: processOnsets(2, convOns(t_onsets.get("1.0", END).split()), ons2))
    b_export = Button(menu_lower, text="Export", command=lambda: processOnsets(1, convOns(t_onsets.get("1.0", END).split()), False, "Custom", edonsw))
    b_clear = Button(menu_lower, text="Clear", command=lambda: t_onsets.delete("1.0", END))

    t_onsets = ScrolledText(edonsw, wrap=WORD)
    t_onsets.pack(expand=1, fill="both")
    t_onsets.focus()

    menu_lower.pack(expand=1, fill="x")
    b_apply.pack(side="left")
    b_export.pack(side="left")
    b_clear.pack(side="right")

    edonsw.config(menu=menu_upper)
    applyWindowStyle(edonsw)
    edonsw.grab_set()

def abError(title, exception):
    if shadderrinf.get()==1:
        mb.showerror(title, format_exc())
    else:
        mb.showerror(title, exception)


def cfgUnlockAll():
    e_bpm.configure(state="normal")
    e_quanavgstrt.configure(state="normal")
    e_quanstrt.configure(state="normal")
    e_quanseglgth.configure(state="normal")
    e_quanrep.configure(state="normal")
    e_quanmask.configure(state="normal")
    e_usestartonsets.configure(state="normal")
    e_seed.configure(state="normal")
    e_trimmin.configure(state="normal")
    e_trimmax.configure(state="normal")

def cfgEmpty():
    cfgUnlockAll()
    e_minSize.delete(0, END)
    e_maxSize.delete(0, END)
    e_reverseChance.delete(0, END)
    e_minPL.delete(0, END)
    e_maxPL.delete(0, END)
    e_stopChance.delete(0, END)
    e_conspause.delete(0, END)
    e_minFadeIn.delete(0, END)
    e_maxFadeIn.delete(0, END)
    e_fadeInChance.delete(0, END)
    e_minFadeOut.delete(0, END)
    e_maxFadeOut.delete(0, END)
    e_fadeOutChance.delete(0, END)
    e_fdprior.delete(0, END)
    e_faderestrict.delete(0, END)
    e_mincrossfade.delete(0, END)
    e_maxcrossfade.delete(0, END)
    e_crossfadechance.delete(0, END)
    e_repeatMin.delete(0, END)
    e_repeatMax.delete(0, END)
    e_repeatchance.delete(0, END)
    e_consrep.delete(0, END)
    e_minsegs.delete(0, END)
    e_maxsegs.delete(0, END)
    e_rememberchance.delete(0, END)
    e_avgstrt.delete(0, END)
    e_strtdev.delete(0, END)
    e_strtweights.delete(0, END)
    e_normStrtChance.delete(0, END)
    e_speeds.delete(0, END)
    e_speedweights.delete(0, END)
    e_fdmode_lc.delete(0, END)
    e_fdmode_sf.delete(0, END)
    e_fdmode_en.delete(0, END)
    e_BackmaskCrossfade.delete(0, END)
    e_BackmaskChance.delete(0, END)
    e_asymmetricalBackmaskChance.delete(0, END)
    e_reverseMaskChance.delete(0, END)
    e_doublesize.delete(0, END)
    e_consecbackmask.delete(0, END)
    e_minMaskRepeat.delete(0, END)
    e_maxMaskRepeat.delete(0, END)
    e_maskRepeatChance.delete(0, END)
    e_stumblechance.delete(0, END)
    e_stumbledeviation.delete(0, END)
    e_stumavgstrt.delete(0, END)
    e_countstumblepauses.delete(0, END)
    e_minfdmsk.delete(0, END)
    e_seed.delete(0, END)
    e_bpm.delete(0, END)
    e_quanavgstrt.delete(0, END)
    e_quanstrt.delete(0, END)
    e_quanseglgth.delete(0, END)
    e_quanrep.delete(0, END)
    e_quanmask.delete(0, END)
    e_usestartonsets.delete(0, END)
    e_trimmin.delete(0, END)
    e_trimmax.delete(0, END)

def cfgDefault():
    e_minSize.insert(0, "0")
    e_maxSize.insert(0, "0")
    c_methDur.current(0)
    e_reverseChance.insert(0, "0")
    e_minPL.insert(0, "0")
    e_maxPL.insert(0, "0")
    c_methPause.current(0)
    e_stopChance.insert(0, "0")
    e_conspause.insert(0, "0")
    e_minFadeIn.insert(0, "0")
    e_maxFadeIn.insert(0, "0")
    c_methFdIn.current(0)
    e_fadeInChance.insert(0, "100")
    e_minFadeOut.insert(0, "0")
    e_maxFadeOut.insert(0, "0")
    c_methFdOut.current(0)
    e_fadeOutChance.insert(0, "100")
    e_fdprior.insert(0, "0")
    e_faderestrict.insert(0, "0")
    e_mincrossfade.insert(0, "0")
    e_maxcrossfade.insert(0, "0")
    c_methCrsfd.current(0)
    e_crossfadechance.insert(0, "100")
    e_repeatMin.insert(0, "0")
    e_repeatMax.insert(0, "0")
    e_repeatchance.insert(0,"0")
    c_methrep.current(0)
    e_consrep.insert(0, "0")
    e_minsegs.insert(0,"0")
    e_maxsegs.insert(0,"0")
    c_remembertype.current(0)
    e_rememberchance.insert(0,"0")
    e_avgstrt.insert(0, "0")
    e_strtweights.insert(0, "1")
    e_strtdev.insert(0, "0")
    e_normStrtChance.insert(0, "0")
    e_speeds.insert(0, "0")
    e_speedweights.insert(0, "1")
    c_TimeMeasure.current(0)
    e_fdmode_lc.insert(0, "1")
    e_fdmode_sf.insert(0, "0")
    e_fdmode_en.insert(0, "0")
    e_BackmaskCrossfade.insert(0, "0")
    e_BackmaskChance.insert(0, "0")
    e_asymmetricalBackmaskChance.insert(0, "0")
    e_reverseMaskChance.insert(0, "0")
    e_doublesize.insert(0, "0")
    e_consecbackmask.insert(0, "100")
    e_minMaskRepeat.insert(0, "0")
    e_maxMaskRepeat.insert(0, "0")
    c_methrepmsk.current(0)
    c_maskmode.current(0)
    e_maskRepeatChance.insert(0, "0")
    e_stumblechance.insert(0, "0")
    e_stumbledeviation.insert(0, "0")
    c_methStumble.current(0)
    e_stumavgstrt.insert(0, "0")
    e_countstumblepauses.insert(0, "0")
    c_propfadein.current(0)
    c_propfadeout.current(0)
    c_repmode.current(0)
    e_minfdmsk.insert(0, "0")
    x_notepropfd.set(0)
    x_fromseed.set(0)
    c_quantizeMode.current(0)
    e_bpm.insert(0, "120")
    e_quanavgstrt.insert(0, "100")
    e_quanstrt.insert(0, "100")
    e_quanseglgth.insert(0, "100")
    e_quanrep.insert(0, "100")
    e_quanmask.insert(0, "100")
    e_usestartonsets.insert(0, "100")
    x_trimfile.set(0)
    e_trimmin.insert(0, "0")
    e_trimmax.insert(0, "0")
    x_shiftons.set(1)

def cfgImport():
    selfile = fd.askopenfilename(filetypes=preset_types, initialdir=abConfig.get("dir_presets"))
    if validPath(selfile):
        try:
            abConfig.set("dir_presets", path=selfile)
            preset = RawConfigParser()
            preset.read(selfile, encoding="utf-8")
            version = preset.get("AudioButcher", "version", fallback="2.1.0")
            if checkVersion(version):
                ab = "AudioButcher"
                cfgEmpty()
                e_minSize.insert(0, preset.get(ab, "minSize", fallback="0"))
                e_maxSize.insert(0, preset.get(ab, "maxSize", fallback="0"))
                cboxSel(c_methDur, preset.get(ab, "methDur", fallback="0"))
                e_reverseChance.insert(0, preset.get(ab, "reverseChance", fallback="0"))
                e_minPL.insert(0, preset.get(ab, "minPL", fallback="0"))
                e_maxPL.insert(0, preset.get(ab, "maxPL", fallback="0"))
                cboxSel(c_methPause, preset.get(ab, "methPause", fallback="0"))
                e_stopChance.insert(0, preset.get(ab, "stopChance", fallback="0"))
                e_conspause.insert(0, preset.get(ab, "conspause", fallback="0"))
                e_minFadeIn.insert(0, preset.get(ab, "minFadeIn", fallback="0"))
                e_maxFadeIn.insert(0, preset.get(ab, "maxFadeIn", fallback="0"))
                cboxSel(c_methFdIn, preset.get(ab, "methFdIn", fallback="0"))
                e_fadeInChance.insert(0, preset.get(ab, "fadeInChance", fallback="0"))
                e_minFadeOut.insert(0, preset.get(ab, "minFadeOut", fallback="0"))
                e_maxFadeOut.insert(0, preset.get(ab, "maxFadeOut", fallback="0"))
                cboxSel(c_methFdOut, preset.get(ab, "methFdOut", fallback="0"))
                e_fadeOutChance.insert(0, preset.get(ab, "fadeOutChance", fallback="0"))
                e_fdprior.insert(0, preset.get(ab, "fdprior", fallback="0"))
                e_faderestrict.insert(0, preset.get(ab, "faderestrict", fallback="0"))
                e_mincrossfade.insert(0, preset.get(ab, "mincrossfade", fallback="0"))
                e_maxcrossfade.insert(0, preset.get(ab, "maxcrossfade", fallback="0"))
                cboxSel(c_methCrsfd, preset.get(ab, "methCrsfd", fallback="0"))
                e_crossfadechance.insert(0, preset.get(ab, "crossfadechance", fallback="0"))
                e_repeatMin.insert(0, preset.get(ab, "repeatMin", fallback="0"))
                e_repeatMax.insert(0, preset.get(ab, "repeatMax", fallback="0"))
                cboxSel(c_methrep, preset.get(ab, "methrep", fallback="0"))
                e_repeatchance.insert(0, preset.get(ab, "repeatchance", fallback="0"))
                e_consrep.insert(0, preset.get(ab, "consrep", fallback="0"))
                e_minsegs.insert(0, preset.get(ab, "minsegs", fallback=0))
                e_maxsegs.insert(0, preset.get(ab, "maxsegs", fallback=0))
                cboxSel(c_remembertype, preset.get(ab, "remembertype", fallback=0))
                e_rememberchance.insert(0, preset.get(ab, "rememberchance", fallback=0))
                e_avgstrt.insert(0, preset.get(ab, "avgstrt", fallback="0"))
                e_strtdev.insert(0, preset.get(ab, "strtdev", fallback="0"))
                e_strtweights.insert(0, preset.get(ab, "strtweights", fallback="1"))
                e_normStrtChance.insert(0, preset.get(ab, "normStrtChance", fallback="0"))
                e_speeds.insert(0, preset.get(ab, "speeds", fallback="0"))
                e_speedweights.insert(0, preset.get(ab, "speedweights", fallback="1"))
                cboxSel(c_TimeMeasure, preset.get(ab, "TimeMeasure", fallback="0"), 1)
                e_fdmode_lc.insert(0, preset.get(ab, "fdmode_lc", fallback="0"))
                e_fdmode_sf.insert(0, preset.get(ab, "fdmode_sf", fallback="0"))
                e_fdmode_en.insert(0, preset.get(ab, "fdmode_en", fallback="0"))
                e_BackmaskCrossfade.insert(0, preset.get(ab, "BackmaskCrossfade", fallback="0"))
                e_BackmaskChance.insert(0, preset.get(ab, "BackmaskChance", fallback="0"))
                e_asymmetricalBackmaskChance.insert(0, preset.get(ab, "asymmetricalBackmaskChance", fallback="0"))
                e_reverseMaskChance.insert(0, preset.get(ab, "reverseMaskChance", fallback="0"))
                e_doublesize.insert(0, preset.get(ab, "doublesize", fallback="0"))
                e_consecbackmask.insert(0, preset.get(ab, "consecbackmask", fallback="100"))
                e_minMaskRepeat.insert(0, preset.get(ab, "minMaskRepeat", fallback="0"))
                e_maxMaskRepeat.insert(0, preset.get(ab, "maxMaskRepeat", fallback="0"))
                cboxSel(c_methrepmsk, preset.get(ab, "methrepmsk", fallback="0"))
                cboxSel(c_maskmode, preset.get(ab, "maskmode", fallback="0"), 1)
                e_maskRepeatChance.insert(0, preset.get(ab, "maskRepeatChance", fallback="0"))
                e_stumblechance.insert(0, preset.get(ab, "stumblechance", fallback="0"))
                e_stumbledeviation.insert(0, preset.get(ab, "stumbledeviation", fallback="0"))
                cboxSel(c_methStumble, preset.get(ab, "methStumble", fallback="0"), 2)
                e_stumavgstrt.insert(0, preset.get(ab, "stumavgstrt", fallback="0"))
                e_countstumblepauses.insert(0, preset.get(ab, "countstumblepauses", fallback="0"))
                cboxSel(c_propfadein, preset.get(ab, "propfadein", fallback="0"), 1)
                cboxSel(c_propfadeout, preset.get(ab, "propfadeout", fallback="0"), 1)
                cboxSel(c_repmode, preset.get(ab, "repmode", fallback="0"), 1)
                e_minfdmsk.insert(0, preset.get(ab, "minfdmsk", fallback="0"))
                x_notepropfd.set(binBool(preset.get(ab, "notepropfd", fallback="0")))
                x_fromseed.set(binBool(preset.get(ab, "fromseed", fallback="0")))
                e_seed.insert(0, preset.get(ab, "seed", fallback=""))
                cboxSel(c_quantizeMode, preset.get(ab, "quantizeMode", fallback="0"), 2)
                e_bpm.insert(0, preset.get(ab, "bpm", fallback="120"))
                e_quanavgstrt.insert(0, preset.get(ab, "quanavgstrt", fallback="100"))
                e_quanstrt.insert(0, preset.get(ab, "quanstrt", fallback="100"))
                e_quanseglgth.insert(0, preset.get(ab, "quanseglgth", fallback="100"))
                e_quanrep.insert(0, preset.get(ab, "quanrep", fallback="100"))
                e_quanmask.insert(0, preset.get(ab, "quanmask", fallback="100"))
                e_usestartonsets.insert(0, preset.get(ab, "usestartonsets", fallback="100"))
                x_trimfile.set(binBool(preset.get(ab, "trimfile", fallback="0")))
                e_trimmin.insert(0, preset.get(ab, "trimmin", fallback="0"))
                e_trimmax.insert(0, preset.get(ab, "trimmax", fallback="0"))
                x_shiftons.set(binBool(preset.get(ab, "shiftons", fallback="1")))
                apply210CompMethod(preset.get(ab, "CompMethod", fallback=None))
                cfgBackcom(version)
                updateSymbols()
        except Exception as e:
            abError("Preset", e)

def cfgApply():
    global minSize, maxSize, methDur, reverseChance
    global minPL, maxPL, methPause, stopChance, conspause
    global minFadeIn, maxFadeIn, methFdIn, fadeInChance
    global minFadeOut, maxFadeOut, methFdOut, fadeOutChance
    global fdprior, faderestrict
    global mincrossfade, maxcrossfade, methCrsfd, crossfadechance
    global repeatMin, repeatMax, methrep, repeatchance, consrep
    global minsegs, maxsegs, remembertype, rememberchance
    global avgstrt, strtweights, strtdev, normStrtChance
    global speeds, speedweights, fdmode_lc, fdmode_sf, fdmode_en 
    global BackmaskCrossfade, BackmaskChance, asymmetricalBackmaskChance, reverseMaskChance, doublesize, consecbackmask
    global minMaskRepeat, maxMaskRepeat, methrepmsk, maskmode, maskRepeatChance 
    global stumblechance, stumbledeviation, methStumble, stumavgstrt, countstumblepauses
    global propfadein, propfadeout, repmode, minfdmsk, notepropfd, fromseed, seed
    global quantizeMode, bpm, quanavgstrt, quanstrt, quanseglgth, quanrep, quanmask, usestartonsets
    global trimfile, trimmin, trimmax, shiftons
    minSize = float(e_minSize.get())
    maxSize = float(e_maxSize.get())
    methDur = c_methDur.current()
    reverseChance = float(e_reverseChance.get())
    minPL = float(e_minPL.get())
    maxPL = float(e_maxPL.get())
    methPause = c_methPause.current()
    stopChance = float(e_stopChance.get())
    conspause = float(e_conspause.get())
    minFadeIn = float(e_minFadeIn.get())
    maxFadeIn = float(e_maxFadeIn.get())
    methFdIn = c_methFdIn.current()
    fadeInChance = float(e_fadeInChance.get())
    minFadeOut = float(e_minFadeOut.get())
    maxFadeOut = float(e_maxFadeOut.get())
    methFdOut = c_methFdOut.current()
    fadeOutChance = float(e_fadeOutChance.get())
    fdprior = float(e_fdprior.get())
    faderestrict = float(e_faderestrict.get())
    mincrossfade = float(e_mincrossfade.get())
    maxcrossfade = float(e_maxcrossfade.get())
    methCrsfd = c_methCrsfd.current()
    crossfadechance = float(e_crossfadechance.get())
    repeatMin = float(e_repeatMin.get())
    repeatMax = float(e_repeatMax.get())
    methrep = c_methrep.current()
    repeatchance = float(e_repeatchance.get())
    consrep = float(e_consrep.get())
    minsegs = float(e_minsegs.get())
    maxsegs = float(e_maxsegs.get())
    remembertype = c_remembertype.current()
    rememberchance = float(e_rememberchance.get())
    avgstrt = list(map(float, e_avgstrt.get().split()))
    strtweights = list(map(int, e_strtweights.get().split()))
    strtdev = float(e_strtdev.get())
    normStrtChance = float(e_normStrtChance.get())
    speeds = list(map(float, e_speeds.get().split()))
    speedweights = list(map(int, e_speedweights.get().split()))
    TimeMeasure = c_TimeMeasure.current()
    fdmode_lc = int(e_fdmode_lc.get())
    fdmode_sf = int(e_fdmode_sf.get())
    fdmode_en = int(e_fdmode_en.get())
    BackmaskCrossfade = float(e_BackmaskCrossfade.get())
    BackmaskChance = float(e_BackmaskChance.get())
    asymmetricalBackmaskChance = float(e_asymmetricalBackmaskChance.get())
    reverseMaskChance = float(e_reverseMaskChance.get())
    doublesize = float(e_doublesize.get())
    consecbackmask = float(e_consecbackmask.get())
    minMaskRepeat = float(e_minMaskRepeat.get())
    maxMaskRepeat = float(e_maxMaskRepeat.get())
    methrepmsk = c_methrepmsk.current()
    maskmode = c_maskmode.current()
    maskRepeatChance = float(e_maskRepeatChance.get())
    stumblechance = float(e_stumblechance.get())
    stumbledeviation = float(e_stumbledeviation.get())
    methStumble = c_methStumble.current()
    stumavgstrt = float(e_stumavgstrt.get())
    countstumblepauses = float(e_countstumblepauses.get())
    propfadein = c_propfadein.current()
    propfadeout = c_propfadeout.current()
    repmode = c_repmode.current()
    minfdmsk = float(e_minfdmsk.get())
    notepropfd = x_notepropfd.get()
    fromseed = x_fromseed.get()
    seed = e_seed.get()
    quantizeMode = c_quantizeMode.current()
    bpm = float(e_bpm.get())
    quanavgstrt = float(e_quanavgstrt.get())
    quanstrt = float(e_quanstrt.get())
    quanseglgth = float(e_quanseglgth.get())
    quanrep = float(e_quanrep.get())
    quanmask = float(e_quanmask.get())
    usestartonsets = float(e_usestartonsets.get())
    trimfile = x_trimfile.get()
    trimmin = float(e_trimmin.get())
    trimmax = float(e_trimmax.get())
    shiftons = x_shiftons.get()
    if TimeMeasure == 1:
        BackmaskCrossfade*=1000
        stumbledeviation*=1000
        minfdmsk*=1000
        avgstrt = [s*1000 for s in avgstrt]
        strtdev*=1000
        trimmin*=1000
        trimmax*=1000
        if methDur!=3:
            minSize*=1000
            maxSize*=1000
        if methPause!=3:
            minPL*=1000
            maxPL*=1000
        if methCrsfd!=3:
            mincrossfade*=1000
            maxcrossfade*=1000
        if methFdIn!=3 and propfadein!=1:
            minFadeIn*=1000
            maxFadeIn*=1000
        if methFdOut!=3 and propfadeout!=1:
            minFadeOut*=1000
            maxFadeOut*=1000
        if repmode==1:
            minsegs*=1000
            maxsegs*=1000
        if maskmode==1:
            minMaskRepeat*=1000
            maxMaskRepeat*=1000

def cfgBackcom(version):
    if version == "2.1.0":
        if e_doublesize.get()=="1":
            e_doublesize.delete(0, END)
            e_doublesize.insert(0, "100")
        version = "2.1.1"
    if version == "2.1.1":
        if e_conspause.get()=="1":
            e_conspause.delete(0, END)
            e_conspause.insert(0, "100")
        if e_consrep.get()=="1":
            e_consrep.delete(0, END)
            e_consrep.insert(0, "100")
        if c_methDur.current()==2: c_methDur.current(3)
        if c_methPause.current()==2: c_methPause.current(3)
        if c_methFdIn.current()==2: c_methFdOut.current(3)
        if c_methFdOut.current()==2: c_methFdOut.current(3)
        if c_methCrsfd.current()==2: c_methCrsfd.current(3)
        if c_methrep.current()==2: c_methrep.current(3)
        if c_methDur.current()==1: c_methDur.current(2)
        if c_methPause.current()==1: c_methPause.current(2)
        if c_methFdIn.current()==1: c_methFdIn.current(2)
        if c_methFdOut.current()==1: c_methFdOut.current(2)
        if c_methCrsfd.current()==1: c_methCrsfd.current(2)
        if c_methrep.current()==1: c_methrep.current(2)
        if c_methrepmsk.current()==1: c_methrepmsk.current(2)
        if c_TimeMeasure.current() != 1:
            _avgstrt = e_avgstrt.get()
            _strtdev = e_strtdev.get()
            e_avgstrt.delete(0, END)
            e_strtdev.delete(0, END)
            for t in _avgstrt.split():
                e_avgstrt.insert(END, sec2ms(t))
                e_avgstrt.insert(END, " ")
            e_strtdev.insert(0, sec2ms(_strtdev))
        version = "2.2.0"
    if version == "2.2.0":
        version == "2.2.1.00"

def cfgExport():
    defname = getNoExt(lastSrcPath)
    if defname!="": defname+=" preset"
    selfile = fd.asksaveasfilename(filetypes=preset_types, defaultextension=preset_types, initialfile=defname, initialdir=abConfig.get("dir_presets"))
    if validPath(selfile):
        try:
            summary = f"""[AudioButcher]
version = {abVersionShort}
minSize = {e_minSize.get()}
maxSize = {e_maxSize.get()}
methDur = {c_methDur.current()}
reverseChance = {e_reverseChance.get()}
minPL = {e_minPL.get()}
maxPL = {e_maxPL.get()}
methPause = {c_methPause.current()}
stopChance = {e_stopChance.get()}
conspause = {e_conspause.get()}
minFadeIn = {e_minFadeIn.get()}
maxFadeIn = {e_maxFadeIn.get()}
methFdIn = {c_methFdIn.current()}
fadeInChance = {e_fadeInChance.get()}
minFadeOut = {e_minFadeOut.get()}
maxFadeOut = {e_maxFadeOut.get()}
methFdOut = {c_methFdOut.current()}
fadeOutChance = {e_fadeOutChance.get()}
fdprior = {e_fdprior.get()}
faderestrict = {e_faderestrict.get()}
mincrossfade = {e_mincrossfade.get()}
maxcrossfade = {e_maxcrossfade.get()}
methCrsfd = {c_methCrsfd.current()}
crossfadechance = {e_crossfadechance.get()}
repeatMin = {e_repeatMin.get()}
repeatMax = {e_repeatMax.get()}
methrep = {c_methrep.current()}
repeatchance = {e_repeatchance.get()}
consrep = {e_consrep.get()}
minsegs = {e_minsegs.get()}
maxsegs = {e_maxsegs.get()}
remembertype = {c_remembertype.current()}
rememberchance = {e_rememberchance.get()}
avgstrt = {e_avgstrt.get()}
strtdev = {e_strtdev.get()}
strtweights = {e_strtweights.get()}
normStrtChance = {e_normStrtChance.get()}
speeds = {e_speeds.get()}
speedweights = {e_speedweights.get()}
TimeMeasure = {c_TimeMeasure.current()}
fdmode_lc = {e_fdmode_lc.get()}
fdmode_sf = {e_fdmode_sf.get()}
fdmode_en = {e_fdmode_en.get()}
BackmaskCrossfade = {e_BackmaskCrossfade.get()}
BackmaskChance = {e_BackmaskChance.get()}
asymmetricalBackmaskChance = {e_asymmetricalBackmaskChance.get()}
reverseMaskChance = {e_reverseMaskChance.get()}
doublesize = {e_doublesize.get()}
consecbackmask = {e_consecbackmask.get()}
minMaskRepeat = {e_minMaskRepeat.get()}
maxMaskRepeat = {e_maxMaskRepeat.get()}
methrepmsk = {c_methrepmsk.current()}
maskmode = {c_maskmode.current()}
maskRepeatChance = {e_maskRepeatChance.get()}
stumblechance = {e_stumblechance.get()}
stumbledeviation = {e_stumbledeviation.get()}
methStumble = {c_methStumble.current()}
stumavgstrt = {e_stumavgstrt.get()}
countstumblepauses = {e_countstumblepauses.get()}
propfadein = {c_propfadein.current()}
propfadeout = {c_propfadeout.current()}
repmode = {c_repmode.current()}
minfdmsk = {e_minfdmsk.get()}
notepropfd = {x_notepropfd.get()}
fromseed = {x_fromseed.get()}
seed = {e_seed.get()}
quantizeMode = {c_quantizeMode.current()}
bpm = {e_bpm.get()}
quanavgstrt = {e_quanavgstrt.get()}
quanstrt = {e_quanstrt.get()}
quanseglgth = {e_quanseglgth.get()}
quanrep = {e_quanrep.get()}
quanmask = {e_quanmask.get()}
usestartonsets = {e_usestartonsets.get()}
trimfile = {x_trimfile.get()}
trimmin = {e_trimmin.get()}
trimmax = {e_trimmax.get()}
shiftons = {x_shiftons.get()}
"""
            abConfig.set("dir_presets", path=selfile)
            preset = open(selfile, "w", encoding="utf-8")
            preset.write(summary)
            preset.close()
        except Exception as e:
            abError("Preset", e)


def checkConfig():
    return checkImportedFile() and checkComboboxes() and checkZeroSegment() and checkWrongRandom() and checkWrongLognorm() and checkWrongSpeeds() and checkWrongStarts() and checkZeroFdModes() and checkTrim() and checkOnsets()

def checkImportedFile():
    if importState=="none":
        mb.showerror("Error", "You have to first load an audio file!")
        return False
    elif importState=="wait":
        mb.showerror("Import", "Please wait while importing!")
        return False
    elif importState=="good":
        return True

def checkComboboxes():
    wrong = -1 in [methDur, methPause, methFdIn, methFdOut, methCrsfd, methrep, remembertype, c_TimeMeasure.current(), methrepmsk, maskmode, methStumble, quantizeMode, propfadein, propfadeout, repmode]
    if wrong: mb.showerror("Error", "Please check all checkboxes!")
    return not wrong

def checkZeroSegment():
    wrong = minSize==0 and maxSize==0
    if wrong: mb.showerror("Error", "Segment length can't be zero!")
    return not wrong

def checkWrongRandom():
    wrong = False
    if methDur==0 and minSize > maxSize: wrong = True
    elif methPause==0 and minPL > maxPL: wrong = True
    elif methrepmsk==0 and minMaskRepeat > maxMaskRepeat: wrong = True
    elif methrep==0 and repeatMin > repeatMax: wrong = True
    elif methCrsfd==0 and mincrossfade > maxcrossfade: wrong = True
    elif methFdIn==0 and minFadeIn > maxFadeIn: wrong = True
    elif methFdOut==0 and minFadeOut > maxFadeOut: wrong = True
    elif remembertype==0 and minsegs > maxsegs: wrong = True
    if wrong: mb.showerror("Error", "In UNIFORM random mode, the first value should be less than the second!")
    return not wrong

def checkWrongLognorm():
    wrong = False
    if methDur==3 and (minSize > 10 or maxSize > 10): wrong = True
    elif methPause==3 and (minPL > 10 or maxPL > 10): wrong = True
    elif methFdIn==3 and (minFadeIn > 10 or maxFadeIn > 10): wrong = True
    elif methFdOut==3 and (minFadeOut > 10 or maxFadeOut > 10): wrong = True
    elif methCrsfd==3 and (mincrossfade > 10 or maxcrossfade > 10): wrong = True
    elif methrep==3 and (repeatMin > 10 or repeatMax > 10): wrong = True
    elif methrepmsk==3 and (minMaskRepeat > 10 or maxMaskRepeat > 10): wrong = True
    elif remembertype==3 and (minsegs > 10 or maxsegs > 10): wrong = True
    if wrong: return mb.askyesno("Warning", "In LOGNORMAL random mode, parameters greater than 10 are not recommended! Continue anyway?", icon="warning")
    else: return True

def checkWrongSpeeds():
    a = len(speeds)
    b = len(speedweights)
    if a!=b: mb.showerror("Error", f"The number of speeds and their weights must match! ({a} vs {b})")
    return a==b

def checkWrongStarts():
    a = len(avgstrt)
    b = len(strtweights)
    if a!=b: mb.showerror("Error", f"The number of average start times and their weights must match! ({a} vs {b})")
    return a==b

def checkZeroFdModes():
    wrong = fdmode_lc==0 and fdmode_sf==0 and fdmode_en==0
    if wrong: mb.showerror("Error", "You must activate at least one fade mode!")
    return not wrong

def checkTrim():
    if trimfile==1 and trimmax<=trimmin:
        return mb.askyesno("Trim", "Trim 'From' is bigger than 'To'. 'To' will be defaulted to length of audio. Continue?", icon="warning")
    else:
        return True

def checkOnsets():
    if quantizeMode==1:
        if binBool(abConfig.get("ignoreonss"))==1:
            mb.showerror("Onsets", "Onsets are currently ignored!")
            return False
        elif onsets==[]:
            if mb.askyesno("Onsets", "You can't use ONSET quantize mode without onsets detected.\nDo you want to detect onsets?", icon="error"): abOnsetsWindow()
            return False
        else:
            return True
    else:
        return True


def genImportAudio(refr=False, raw=False):
    global audio, lastSrcPath, lastSrcIsRaw
    if refr:
        selfile = lastSrcPath
        raw = lastSrcIsRaw
    else:
        if raw: types = []
        else: types = import_types
        selfile = fd.askopenfilename(filetypes=types, initialdir=abConfig.get("dir_srcaud"))
    if raw and validPath(selfile): rawcfg = genAskRawParameters()
    if validPath(selfile) and (not raw or rawcfg!=None):
        abConfig.set("dir_srcaud", path=selfile)
        importstate("wait")
        try:
            lastSrcPath = selfile
            lastSrcIsRaw = raw
            if raw: audio = AudioSegment.from_raw(selfile, sample_width=rawcfg[0], channels=rawcfg[1], frame_rate=rawcfg[2])
            else: audio = loadAudio(selfile)
        except Exception as e:
            importstate("none"); updateWindow()
            abError("Import", e)
        else:
            if resetonsets.get()==1:
                processOnsets(2, [])
                processOnsets(2, [], True)
            if autoonsdet.get()==1: getOnsets(None, 2, fromCurrent=True, window=False)
            importstate("good"); updateWindow()
            if not raw or rawcfg!=None: mb.showinfo("Import", "Audio imported successfully.")

def genAskRawParameters():
    class rawDialog:
        def __init__(self, parent):
            self._return = None
            sw_variants = ["8-bit", "16-bit", "24-bit", "32-bit"]
            cs_variants = ["1", "2"]
            fr_variants = ["8000", "11025", "16000", "22050", "32000", "44100", "48000", "88200", "96000", "176400", "192000", "352800", "384000"]

            self.box = Toplevel(parent)
            self.box.title("")
            face = Frame(self.box, padding=3)
            face.pack(side="top", fill="x")
            buts = Frame(self.box, padding=1)
            buts.pack(side="bottom", fill="x")

            Label(face, text="Sample width: ").grid(column=0, row=0, sticky="w")
            Label(face, text="Channels: ").grid(column=0, row=1, sticky="w")
            Label(face, text="Frame rate: ").grid(column=0, row=2, sticky="w")

            self.samplewidth = Combobox(face, width=10, state="readonly", values=sw_variants)
            self.channels = Combobox(face, width=10, values=cs_variants)
            self.framerate = Combobox(face, width=10, values=fr_variants)

            self.samplewidth.grid(column=1, row=0, sticky="e")
            self.channels.grid(column=1, row=1, sticky="e")
            self.framerate.grid(column=1, row=2, sticky="e")

            cboxSel(self.samplewidth, abConfig.get("raw_def_sw"), 3)
            self.channels.insert(0, abConfig.get("raw_def_cs"))
            self.framerate.insert(0, abConfig.get("raw_def_fr"))

            Button(buts, text="OK", command=lambda: self.onOkay()).pack(side="left")
            Button(buts, text="Cancel", command=lambda: self.onCancel()).pack(side="right")

            applyWindowStyle(self.box)
            self.box.grab_set()
            self._return = None
        def onOkay(self):
            try:
                self._return = [self.samplewidth.current()+1, int(self.channels.get()), int(self.framerate.get())]
                abConfig.set("raw_def_sw", self._return[0]-1)
                abConfig.set("raw_def_cs", self._return[1])
                abConfig.set("raw_def_fr", self._return[2])
                if self._return[2]==0: 0/0 #Raise an error
            except Exception:
                self._return = None
                mb.showerror("Raw Data", "Wrong settings!", parent=self.box)
            else:
                self.box.destroy()
        def onCancel(self):
            self._return = None
            self.box.destroy()

    dialog = rawDialog(window)
    window.wait_window(dialog.box)
    return dialog._return

def genScramble(export, segTime):
    global generating, genTime
    try:
        cfgApply()
    except Exception as e:
        abError("Configuration", e)
    else:
        if segTime!=None and checkConfig() and (not previewing or export) and not generating:
            if export: selfile = fd.asksaveasfilename(filetypes=export_types, defaultextension=export_types, initialfile=newFileName(), initialdir=abConfig.get("dir_resaud"))
            else: selfile = None
            if validPath(selfile) or not export:
                genTime = segTime
                if export:
                    abConfig.set("dir_resaud", path=selfile)
                    abConfig.set("ste", round(segTime))
                try:
                    generating = True; b_abort.configure(state="normal")
                    slicecr = genMain(audio, segTime, onsets, onsets2)
                    generating = False; b_abort.configure(state="disabled")
                except Exception as e:
                    generating = False; b_abort.configure(state="disabled")
                    abError("Scrambling", e)
                else:
                    if export:
                        try:
                            slicecr.export(selfile, format="wav")
                        except Exception as e:
                            abError("Export", e)
                        else:
                            if mb.askyesno("Complete!", "Scrambling complete.\nDo you want to open your file now?", icon="info"): openFile(selfile)
                    else:
                        run(genPreview, slicecr, segTime)
                finally:
                    progress["value"]=0

def genPreview(audio, time):
    global previewing
    try:
        previewing = True; updateWindow()
        supportedFrs = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
        if time > audio.duration_seconds: time = audio.duration_seconds
        if audio.sample_width > 3: audio = audio.set_sample_width(2)
        if not audio.frame_rate in supportedFrs: audio = audio.set_frame_rate(findNearest(supportedFrs, audio.frame_rate, 0))
        if audio.channels > 2: audio = audio.set_channels(1)
        play(audio[0:time*1000])
    except Exception as e:
        abError("Preview", e)
    finally:
        previewing = False; updateWindow()

def genStopPreview():
    global previewing
    if not AB_DISABLE_SIMPLEAUDIO:
        simpleaudio.stop_all()

def genAbort():
    global generating
    generating = not mb.askyesno("Abort", f"Are you sure you want to abort scrambling?\nThe current rendered length is {round(genReady, 3)} seconds out of {genTime} ({round(genReady/genTime*100, 2)}%).\nAudio will be exported/previewed anyway.", icon="warning")

def genRandNum(val1, val2, mode):
    if mode == 0: return random.uniform(val1, val2)
    elif mode == 1:
        fval = -1
        while fval < 0:
            fval = random.gauss(val1,val2)
        return fval
    elif mode == 2: return abs(random.gauss(val1,val2))
    elif mode == 3: return random.lognormvariate(val1,val2)

def genMain(audio, segTime, onsets, onsets2):
    global genReady
    global minfdmsk, trimmin, trimmax
    
    if fromseed==1:
        random.seed(seed)
    else:
        random.seed()
    
    lengthOfAudio = audio.duration_seconds*1000
    if trimfile==1:
        if trimmin < 0: trimmin = 0
        if trimmax > lengthOfAudio or trimmax<=trimmin: trimmax = lengthOfAudio
        audio = audio[trimmin:trimmax]
        if shiftons==1: 
            onsets = [o-trimmin for o in onsets if trimmin<=o<=trimmax]
            onsets2 = [o-trimmin for o in onsets2 if trimmin<=o<=trimmax]
        lengthOfAudio = audio.duration_seconds*1000

    if binBool(abConfig.get("ignoreonss"))==1: onsets = []
    if binBool(abConfig.get("ignoreons2"))==1: onsets2 = []

    if quantizeMode != 1:
        onsets2 = []

    if quantizeMode == 2:
        i = 1
        onsets = [0]
        while (i * 60/bpm * 1000) <= audio.duration_seconds*1000:
            onsets.append(i * 60/bpm * 1000)
            i += 1

    slicecr = AudioSegment.silent(duration = 1) #make slicecr audio that we can work with

    counter = 0
    firstTime = 1
    stumblestrt = 0

    print("\nnewgen\n")

    if stumblechance > 0:
        audio += audio[0:0.1*lengthOfAudio]  #1.1x audio length to help prevent stumbling over file end
        newaudlgth = audio.duration_seconds*1000

    if quantizeMode != 0:
        lengthOfAudio = findNearest(onsets, lengthOfAudio, 0)

    paused = 0
    stumbpause = 0
    chance = 0
    fadepause = 0
    repeated = 0
    rembintialized = 0
    backmasked = 0

    #check if minfademask is needed
    if propfadeout == 1 and notepropfd == 1:
        minfdmsk = 0
    
    genReady = 0
    while slicecr.duration_seconds < segTime and generating:
        firstchance = random.uniform(0,100)
        inchance = random.uniform(0,100)
        outchance = random.uniform(0,100)
        crosschance = random.uniform(0,100)
        revchance = random.uniform(0,100)
        bkmskchance = random.uniform(0,100)
        repchance = random.uniform(0,100)
        nrmSrtChnce = random.uniform(0,100)
        stumbchnce = random.uniform(0,100)
        asymmaskchnce = random.uniform(0,100)
        doublsize = random.uniform(0,100)
        quanstrtchnce = random.uniform(0,100)
        quanseglgthchnce = random.uniform(0,100)
        quanavgstrtchnce = random.uniform(0,100)
        remberchnce = random.uniform(0,100)
        conspausechce = random.uniform(0,100)
        consrepchce = random.uniform(0,100)
        consbckmskchce = random.uniform(0,100)
        fdpriorchce = random.uniform(0,100)
        quanrepchce = random.uniform(0,100)
        quanmaskchce = random.uniform(0,100)
        faderestrictchce = random.uniform(0,100)
        stumavgstrtchce = random.uniform(0,100)
        countstumblepauseschce = random.uniform(0,100)
        usestartonsetschce = random.uniform(0,100)

        if not(firstchance < (100 - stopChance)):
            fadepause = 1
        else: 
            fadepause = 0

        averagestart = random.choices(avgstrt, weights=strtweights)[0]
        speed = random.choices(speeds, weights=speedweights)[0]
        CompMethod = random.choices([0, 1, 2], weights=[fdmode_lc, fdmode_sf, fdmode_en])[0]

        if crosschance < crossfadechance:
            crossfade = genRandNum(mincrossfade, maxcrossfade, methCrsfd)
            if crossfade < 1 and crossfade > 0: crossfade = 1
            crossfade = int(crossfade)
        else:
            crossfade = 0

        if firstTime == 1:                                      #check if it's first loop
            slicecr = AudioSegment.silent(duration = crossfade) #make silence length equal crossfade
            slicecr = slicecr.set_frame_rate(audio.frame_rate)  #defaults to 11025 for some reason. set to track rate.
            firstTime = 0
            placecross = -1
            placecross2 = -1



        spedcross = int(crossfade * (2**(speed/12)))
        if onsets == []:
            placeonsets = 0
        elif placecross != spedcross:
            placeonsets = onsets.copy()
            placecross = spedcross
            for x in range(len(placeonsets)):
                placeonsets[x] -= spedcross
                if placeonsets[x] < 0: placeonsets[x] = 0

        spedcross2 = int(crossfade * (2**(speed/12)))
        if onsets2 == []:
            placeonsets2 = 0
        elif placecross2 != spedcross2:
            placeonsets2 = onsets2.copy()
            placecross2 = spedcross2
            for x in range(len(placeonsets2)):
                placeonsets2[x] -= spedcross2
                if placeonsets2[x] < 0: placeonsets2[x] = 0


        if nrmSrtChnce < normStrtChance:
            startPosition = -1
            nrmstrtcounter = 0
            while (startPosition < 0 or startPosition >= lengthOfAudio) and nrmstrtcounter < 1000:
                startPosition = random.gauss(averagestart,strtdev)
                nrmstrtcounter += 1
            if nrmstrtcounter == 1000:
                startPosition = random.gauss(averagestart,strtdev)%lengthOfAudio
        else:
            startPosition = random.uniform(0,lengthOfAudio)

        def quantstart(startPosition, direction = 0):
            if quanstrtchnce < quanstrt and quantizeMode > 0 and (not(nrmSrtChnce < normStrtChance) or quanavgstrtchnce < quanavgstrt):
                if direction == 0 and stumbchnce < stumblechance and (not nrmSrtChnce < normStrtChance) and  methStumble == 1: direction = 2
                if placeonsets2 != 0 and usestartonsetschce < usestartonsets and not(stumbchnce < stumblechance and  methStumble == 0):
                    startIndex = findNearest(placeonsets2, startPosition, 1, direction)
                    if startIndex == (len(placeonsets2)-1): startIndex = 0
                    startPosition = placeonsets2[startIndex]
                else:
                    startIndex = findNearest(placeonsets, startPosition, 1, direction)
                    if startIndex == (len(placeonsets)-1): startIndex = 0
                    startPosition = placeonsets[startIndex]
            return startPosition

        startPosition = quantstart(startPosition)


        randdur = genRandNum(minSize, maxSize, methDur)
        if bkmskchance < BackmaskChance and doublsize < doublesize:
            randdur *= 2
        randdur += spedcross
        while randdur <= spedcross*2: randdur += spedcross

        if lengthOfAudio - startPosition < randdur and not(stumbchnce < stumblechance):
            startPosition = lengthOfAudio - randdur

        pause = genRandNum(minPL, maxPL, methPause)
        pause += spedcross

        fadein = 0
        if inchance < fadeInChance and propfadein == 0:
            fadein = int(genRandNum(minFadeIn, maxFadeIn, methFdIn))

        fadeout = 0
        if outchance < fadeOutChance and propfadeout == 0:
            fadeout = int(genRandNum(minFadeOut, maxFadeOut, methFdOut))


        if randdur < fadein + fadeout: #if possible fade times are longer than duration, increase duration to fade times
            if CompMethod == 0 or (CompMethod == 2 and bkmskchance < BackmaskChance):
                randdur = fadein + fadeout + spedcross
            elif CompMethod == 1:
                if fadein > randdur/2:
                    fadein = int(randdur/2)
                if fadeout > randdur/2:
                    fadeout = int(randdur/2)

        repeatcounter = genRandNum(repeatMin, repeatMax, methrep)
        if repmode == 0:
            if repeatcounter < 1 and repeatcounter > 0:
                repeatcounter = 1
        else: repeatcounter += spedcross
        repeatcounter = int(repeatcounter)

        maskrepeatcounter = genRandNum(minMaskRepeat, maxMaskRepeat, methrepmsk)
        if maskmode == 0:
            if maskrepeatcounter < 1 and maskrepeatcounter > 0:
                maskrepeatcounter = 1
            maskrepeatcounter = int(maskrepeatcounter)


        if stumbchnce < stumblechance and (not nrmSrtChnce < normStrtChance):
            if methStumble == 0:
                startPosition = abs(random.gauss(stumblestrt,stumbledeviation))
            elif methStumble == 1:
                startPosition = stumblestrt + abs(random.gauss(0,stumbledeviation))
            elif methStumble == 2:
                startPosition = stumblestrt - abs(random.gauss(0,stumbledeviation))
            if stumbledeviation > 0:
                if methStumble == 2: startPosition = quantstart(startPosition, 1)
                else:  startPosition = quantstart(startPosition)
                


        if stumblechance > 0:
            if newaudlgth - startPosition < randdur:
                startPosition = newaudlgth - randdur


        if quanseglgthchnce < quanseglgth and quantizeMode > 0 and (nrmSrtChnce < normStrtChance or (not(stumbchnce < stumblechance) or stumbledeviation > 0 or methStumble != 1)):
            segIndex = findNearest(placeonsets, startPosition + randdur * (2**(speed/12)), 1)
            randdur = placeonsets[segIndex] - startPosition + spedcross
            while randdur <= spedcross + 0.1:
                segIndex += 1
                if segIndex < len(placeonsets): randdur = placeonsets[segIndex] - startPosition + spedcross
                else: break
            endPosition = startPosition + randdur
        else: endPosition = startPosition + randdur * (2**(speed/12))

        randdurpremask = randdur
        if bkmskchance < BackmaskChance and backmasked == 0: randdur += round(BackmaskCrossfade/2 + .5) * 2
        #fixes offsets in stage three distortions

        if quanrepchce < quanrep and quantizeMode > 0 and repmode == 1:
            repIndex = findNearest(placeonsets, startPosition + randdur + repeatcounter * (2**(speed/12)), 1)
            repeatcounter = placeonsets[repIndex] - (startPosition + randdur) + spedcross
            while repeatcounter <= spedcross:
                repIndex += 1
                if repIndex < len(placeonsets): repeatcounter = placeonsets[repIndex] - (startPosition + randdur) + crossfade
                else: break

        if quanmaskchce < quanmask and quantizeMode > 0 and maskmode == 1:
            maskIndex = findNearest(placeonsets, startPosition + randdurpremask + maskrepeatcounter * (2**(speed/12)), 1)
            maskrepeatcounter = placeonsets[maskIndex] - (startPosition + randdurpremask) + BackmaskCrossfade*2
            while maskrepeatcounter <= BackmaskCrossfade*2:
                maskIndex += 1
                if maskIndex < len(placeonsets): maskrepeatcounter = placeonsets[maskIndex] - (startPosition + randdurpremask) + BackmaskCrossfade*2
                else: break


        #rember
        rembseg = 0
        if remberchnce < rememberchance and rembintialized == 0:
            rembstartPosition = startPosition
            rembranddur = randdurpremask
            rembendPosition = endPosition
            rembcountdown = genRandNum(minsegs, maxsegs, remembertype)
            if rembcountdown < 1 and rembcountdown > 0:
                rembcountdown = 1
            rembcountdown = int(rembcountdown)
            rembintialized = 1
        elif rembintialized == 1 and rembcountdown > 0: rembcountdown -= 1
        elif rembintialized == 1 and  rembcountdown <= 0:
            startPosition = rembstartPosition
            randdur = rembranddur
            endPosition = rembendPosition
            rembintialized = 0
            rembseg = 1

        #create appender segment
        
        if chance < (100 - stopChance) or paused == 1:

            if quanseglgthchnce < quanseglgth and quantizeMode > 0: appender = audio[startPosition:startPosition + randdur]
            else: appender = audio[startPosition:startPosition + randdur * (2**(speed/12))]    #get audio segment, apply speed change if neccesary

            #apply speed change
            appender = speedChange(appender,speed)


            #little crossfade shortener for fadecomp2
            def apcrsfd(audio, audio1 = audio):
                apfd = crossfade
                mintime = min(int(1000*audio.duration_seconds),int(1000*audio1.duration_seconds))
                if apfd > mintime:
                    apfd = mintime
                    #print("fade crossfade shortened")
                return apfd


            #calculate fades for proportional fade modes using appender length 
            fadaplength = 1000*appender.duration_seconds + crossfade
            if inchance < fadeInChance and propfadein == 1:
                fadein = round(genRandNum(minFadeIn, maxFadeIn, methFdIn) * fadaplength/100)
                if fadein > fadaplength and CompMethod != 2: fadein = round(fadaplength)

            if outchance < fadeOutChance and propfadeout == 1:
                fadeout = round(genRandNum(minFadeOut, maxFadeOut, methFdOut) * fadaplength/100)
                if fadeout > fadaplength and CompMethod != 2: fadeout = round(fadaplength)

            #extend segment/note via backmasking for fade compensation 2
            if CompMethod == 2 and not(bkmskchance < BackmaskChance):
                appenderlength = 1000*appender.duration_seconds
                if faderestrictchce > faderestrict or ((fadepause == 1 and not(revchance < reverseChance)) or (paused == 1 and revchance < reverseChance)):
                    if fadeout > 0:
                        if placeonsets != 0:

                            fdsegIndex = findNearest(placeonsets, startPosition + randdur * (2**(speed/12)), 1)
                            shitdur = placeonsets[fdsegIndex] - startPosition + spedcross
                            while shitdur < randdur and fdsegIndex < len(placeonsets)-1:
                                fdsegIndex += 1
                                shitdur = placeonsets[fdsegIndex] - startPosition + spedcross
                            if fdsegIndex > 0:
                                while (endPosition - placeonsets[fdsegIndex - 1] + spedcross <= minfdmsk) or (placeonsets[fdsegIndex - 1] >= int(endPosition)):
                                    fdsegIndex -= 1
                                    if fdsegIndex == 0: break

                            if fdsegIndex > 0: fademask1 = audio[placeonsets[fdsegIndex - 1]:endPosition]
                            else: fademask1 = audio[0:endPosition]


                            fademask1 = speedChange(fademask1,speed)
                            fademask1 = fademask1[0:int(1000*fademask1.duration_seconds)]

                            #change fade to percent of note length if proportional to notes is checked
                            if propfadeout == 1 and notepropfd == 1:
                                fadeout = round(genRandNum(minFadeOut, maxFadeOut, methFdOut) * int(1000*fademask1.duration_seconds)/100)


                            #check if fadeout is 0 again due to it now possibly being a fraction of last note
                            if fadeout > 0:
                                fademask2 = fademask1.reverse()
                                if audio.channels == 2:
                                    fademask2 = fademask2.split_to_mono()        #reversing switches channels for some reason
                                    fademask2 = AudioSegment.from_mono_audiosegments(fademask2[1], fademask2[0])

                                fademask = fademask2.append(fademask1, crossfade=apcrsfd(fademask1))

                                while 1000*fademask.duration_seconds < fadeout:
                                    fademask = fademask.append(fademask, crossfade=apcrsfd(fademask))


                                appender = appender.append(fademask, crossfade=apcrsfd(fademask,appender))
                                appender = appender[0:appenderlength+fadeout]
                                appender = appender.fade_out(fadeout)
                        else:

                            fademask1 = appender
                            fademask2 = fademask1.reverse()
                            if audio.channels == 2:
                                fademask2 = fademask2.split_to_mono()        #reversing switches channels for some reason
                                fademask2 = AudioSegment.from_mono_audiosegments(fademask2[1], fademask2[0])

                            fademask = fademask2.append(fademask1, crossfade=apcrsfd(fademask1))
                            while 1000*fademask.duration_seconds < fadeout:
                                fademask = fademask.append(fademask, crossfade=apcrsfd(fademask))
                                print("loop 2 ",1000*fademask.duration_seconds)
                                
                            appender = appender.append(fademask, crossfade=apcrsfd(appender))
                            appender = appender[0:appenderlength+fadeout]
                            appender = appender.fade_out(fadeout)

                #fade in + regular compensation for compmethod 2 mode
                if faderestrictchce > faderestrict or ((paused == 1 and not(revchance < reverseChance)) or (fadepause == 1 and revchance < reverseChance)):
                    if fadein > 1000*appender.duration_seconds: fadein = round(1000*appender.duration_seconds)
                    if fadein > 0 and not(bkmskchance < BackmaskChance): appender = appender.fade_in(fadein)


            #trim segment to nearest ms (unless non-forwards stumble)
            if not(stumbchnce < stumblechance) or (methStumble == 1) or nrmSrtChnce < normStrtChance:
              appender = appender[0:int(1000*appender.duration_seconds)]

            #repeating
            if repchance <= repeatchance and repeated == 0 and (not(bkmskchance < BackmaskChance and asymmaskchnce >= asymmetricalBackmaskChance)):
                appendercopy = appender
                if repmode == 0:
                    while repeatcounter > 0:
                        appender = appender.append(appendercopy, crossfade=crossfade)
                        repeatcounter -= 1
                else:
                    while appender.duration_seconds*1000 < randdur + repeatcounter - crossfade:
                        appender = appender.append(appendercopy, crossfade=crossfade)
                    appender = appender[0:randdur + repeatcounter - crossfade]
                if consrepchce > consrep: repeated = 1
            else:
                repeated = 0

            #backmasking
            if bkmskchance < BackmaskChance and backmasked == 0:
                bckmskfde = BackmaskCrossfade
                if asymmaskchnce >= asymmetricalBackmaskChance:

                    appender = appender[0:randdur/2]

                    if revchance < reverseMaskChance:
                        appender = appender.reverse()
                        if appender.channels == 2:
                            appender = appender.split_to_mono()        #reversing switches channels for some reason
                            appender = AudioSegment.from_mono_audiosegments(appender[1], appender[0])

                    revpender = appender.reverse()
                    if appender.channels == 2:
                        revpender = revpender.split_to_mono()        #reversing switches channels for some reason
                        revpender = AudioSegment.from_mono_audiosegments(revpender[1], revpender[0])

                    if bckmskfde > appender.duration_seconds*1000:
                        bckmskfde = int(appender.duration_seconds*1000)

                    appender = appender.append(revpender, crossfade=bckmskfde)

                    if repchance <= maskRepeatChance:
                        temppender = appender
                        if maskmode == 0:
                            randdurmult = maskrepeatcounter
                            while maskrepeatcounter > 0:
                                appender = appender.append(temppender, crossfade=bckmskfde)
                                maskrepeatcounter -= 1
                            appender = appender[0:randdurpremask*randdurmult] #requantizes segment
                        else:
                            while appender.duration_seconds*1000 < randdurpremask + maskrepeatcounter:
                                appender = appender.append(temppender, crossfade=bckmskfde)
                            appender = appender[0:randdurpremask + maskrepeatcounter - bckmskfde*2]
                    else: 
                        appender = appender[0:randdurpremask] #requantizes segment
                else:
                    appendlength = appender.duration_seconds*1000

                    if revchance < reverseMaskChance:
                        appender = appender.reverse()
                        if appender.channels == 2:
                            appender = appender.split_to_mono()        #reversing switches channels for some reason
                            appender = AudioSegment.from_mono_audiosegments(appender[1], appender[0])

                    revpender = appender.reverse()
                    if appender.channels == 2:
                        revpender = revpender.split_to_mono()        #reversing switches channels for some reason
                        revpender = AudioSegment.from_mono_audiosegments(revpender[1], revpender[0])

                    if bckmskfde > appender.duration_seconds*1000:
                        bckmskfde = int(appender.duration_seconds*1000)

                    appender = appender.append(revpender, crossfade=bckmskfde)
                    tempstrt = random.uniform(0,appendlength)
                    appender = appender[tempstrt:tempstrt + appendlength]
                if consbckmskchce > consecbackmask: backmasked = 1
            else: backmasked = 0

            if fdpriorchce < fdprior:
                #apply fades
                if CompMethod != 2 or bkmskchance < BackmaskChance:
                    if faderestrictchce > faderestrict or ((paused == 1 and not(revchance < reverseChance)) or (fadepause == 1 and revchance < reverseChance)):
                        if fadein > 0: appender = appender.fade_in(fadein)
                    if faderestrictchce > faderestrict or ((fadepause == 1 and not(revchance < reverseChance)) or (paused == 1 and revchance < reverseChance)):
                        if fadeout > 0: appender = appender.fade_out(fadeout)

            #apply reverse if applicable
            if revchance < reverseChance and not(bkmskchance < BackmaskChance):
                appender = appender.reverse()
                if appender.channels == 2:
                    appender = appender.split_to_mono()        #reversing switches channels for some reason
                    appender = AudioSegment.from_mono_audiosegments(appender[1], appender[0])

            if not(fdpriorchce < fdprior):
                #apply fades
                if CompMethod != 2 or bkmskchance < BackmaskChance:
                    if faderestrictchce > faderestrict or paused == 1:
                        if fadein > 0: appender = appender.fade_in(fadein)
                    if faderestrictchce > faderestrict or fadepause == 1:
                        if fadeout > 0: appender = appender.fade_out(fadeout)


            paused = 0
            stumbpause = 0
            fadepause = 0
            chance = firstchance
        else:
            #add silence to file
            appender = AudioSegment.silent(duration=pause)
            if conspausechce > conspause: paused = 1
            stumbpause = 1
            chance = firstchance

        if (not nrmSrtChnce < normStrtChance) or (not stumavgstrtchce < stumavgstrt):
            if methStumble == 0:
                stumblestrt += (appender.duration_seconds*1000 - crossfade) * (2**(speed/12))
            elif methStumble == 1 and (stumbpause == 0 or countstumblepauseschce < countstumblepauses) and rembseg == 0:
                stumblestrt = startPosition + (appender.duration_seconds*1000 - crossfade) * (2**(speed/12))
            elif methStumble == 2 and (stumbpause == 0 or countstumblepauseschce < countstumblepauses) and rembseg == 0:
                stumblestrt = startPosition - (appender.duration_seconds*1000 - crossfade) * (2**(speed/12))


        stumblestrt = stumblestrt % lengthOfAudio

        if crossfade > appender.duration_seconds*1000:
            crossfade = int(appender.duration_seconds*1000)
            print("crossfade shortened to ", crossfade)
        if crossfade > slicecr.duration_seconds*1000:
            crossfade = int(slicecr.duration_seconds*1000)
            print("crossfade shortened to ", crossfade)
        
        #append segment to final variable
        slicecr = slicecr.append(appender, crossfade=crossfade)

        #debug second/segment counter
        counter +=1
        genReady = slicecr.duration_seconds
        progress["value"]=genReady/segTime*100

    return slicecr

if True:
    importState = "none"
    lastSrcPath = ""
    lastSrcIsRaw = False
    onsets = []
    onsets2 = []
    generating = False
    previewing = False
    genReady = 0

    randmodes = ["Uniform", "Normal", "Folded normal", "Lognorm (µ, σ)"]
    timemodes = ["Milliseconds", "Seconds"]
    repmeasmodes = ["Times", "Length"]
    stumbmodes = ["Standard", "Forwards only", "Backwards only"]
    quantmodes = ["None", "Onsets", "BPM"]
    propfademodes = ["Length", "%s"]

    import_types = [["Popular formats", "*.wav *.mp3 *.ogg *.flac"],
                    ["Wave", "*.wav"],
                    ["MPEG Layer-3", "*.mp3"],
                    ["Ogg Vorbis", "*.ogg"],
                    ["FLAC", "*.flac"],
                    ["All files", "*.*"]]

    export_types = [["Wave", "*.wav"],
                    ["All files", "*.*"]]

    preset_types = [["AudioButcher Preset", "*.abp"],
                    ["All files", "*.*"]]

    onset_types = [["AudioButcher Onset List", "*.abo"],
                   ["Text files", "*.txt"],
                   ["All files", "*.*"]]

    abConfig = abConfigure(join(homepath, ".audiobutcher"), "AudioButcher_Config")

    # Window
    window = Tk()
    tabs = Notebook(window)
    tab1 = Frame(tabs, padding=10)
    tab2 = Frame(tabs, padding=10)
    tabs.add(tab1, text="Main")
    tabs.add(tab2, text="Advanced")
    tabs.pack(expand=1, fill="both", side="top")

    # Menus
    menu = Menu(window)
    window.config(menu=menu)
    menu_file = Menu(menu, tearoff=False)
    menu_prev = Menu(menu, tearoff=False)
    smenu_stp = Menu(menu_prev, tearoff=False)
    menu_pref = Menu(menu, tearoff=False)
    menu_debg = Menu(menu, tearoff=False)
    menu_help = Menu(menu, tearoff=False)
    menu.add_cascade(label="File", menu=menu_file)
    if not AB_DISABLE_SIMPLEAUDIO: menu.add_cascade(label="Preview", menu=menu_prev)
    menu.add_cascade(label="Preferences", menu=menu_pref)
    if AB_DEBUG_BUTTON: menu.add_cascade(label="Debug", menu=menu_debg)
    menu.add_cascade(label="Help", menu=menu_help)

    # File menu
    menu_file.add_command(label="Import audio file...", accelerator="Ctrl+I", command=lambda: run(genImportAudio))
    menu_file.add_command(label="Import raw data...", accelerator="Ctrl+Shift+I", command=lambda: run(genImportAudio, False, True))
    menu_file.add_command(label="Export audio...", accelerator="Ctrl+E", command=lambda: run(genScramble, True, getExportLength()))
    menu_file.add_command(label="Refresh file", accelerator="Ctrl+R", command=lambda: run(genImportAudio, True))
    menu_file.add_separator()
    menu_file.add_command(label="Open preset...", accelerator="Ctrl+O", command=lambda: cfgImport())
    menu_file.add_command(label="Save preset...", accelerator="Ctrl+S", command=lambda: cfgExport())
    menu_file.add_command(label="Clear all settings", accelerator="Ctrl+N", command=lambda: abDefaultConfig())
    menu_file.add_separator()
    menu_file.add_command(label="Quit", command=lambda: sys.exit())

    # Preview menu
    menu_prev.add_command(label="Preview", accelerator="Ctrl+P", command=lambda: run(genScramble, False, stp.get()))
    menu_prev.add_command(label="Stop preview", accelerator="Ctrl+Alt+P", command=lambda: genStopPreview(), state="disabled")
    menu_prev.add_cascade(label="Preview length", menu=smenu_stp)

    # Preview length submenu
    stp = IntVar()
    smenu_stp.add_radiobutton(label="5 seconds",  var=stp, value=5,  command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="10 seconds", var=stp, value=10, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="20 seconds", var=stp, value=20, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="30 seconds", var=stp, value=30, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="40 seconds", var=stp, value=40, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="50 seconds", var=stp, value=50, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="60 seconds", var=stp, value=60, command=lambda: abConfig.set("stp"))
    stp.set(int(abConfig.get("stp")))

    # Preferences menu (variables)
    useunixfilename = IntVar()
    secimpaudlen = IntVar()
    shadderrinf = IntVar()
    autoonsdet = IntVar()
    resetonsets = IntVar()
    closeonsets = IntVar()

    # Preferences menu
    menu_pref.add_checkbutton(label="Generate unique filenames", var=useunixfilename, command=lambda: abConfig.set("useunixfilename"))
    menu_pref.add_checkbutton(label="Imported audio length in seconds", var=secimpaudlen, command=lambda: updSecImpAudLen())
    menu_pref.add_checkbutton(label="Show additional error information", var=shadderrinf, command=lambda: abConfig.set("shadderrinf"))
    menu_pref.add_separator()
    menu_pref.add_checkbutton(label="Automatically detect onsets", var=autoonsdet, command=lambda: abConfig.set("autoonsdet"))
    menu_pref.add_checkbutton(label="Reset onsets after new file imported", var=resetonsets, command=lambda: abConfig.set("resetonsets"))
    menu_pref.add_checkbutton(label="Automatically close onsets window", var=closeonsets, command=lambda: abConfig.set("closeonsets"))
    if AB_DISABLE_LIBROSA: menu_pref.entryconfig(4, state="disabled")

    #Debug menu
    menu_debg.add_command(label="exec", command=lambda: abDebug(False))
    menu_debg.add_command(label="eval", command=lambda: abDebug(True))

    #Help menu
    menu_help.add_command(label="Join our Discord server", command=lambda: abJoinDiscord())
    menu_help.add_separator()
    menu_help.add_command(label="License...", command=lambda: abShowLicense())
    menu_help.add_command(label="About...", command=lambda: abAbout())

    # Main tab
    tab1_sep1 = Label(tab1)
    tab1_sep2 = Label(tab1)
    tab1_sep3 = Label(tab1)
    tab1_sep4 = Label(tab1)

    l_Size = Label(tab1, text="Segment length: ")
    e_minSize = Entry(tab1, width=5)
    s_Size = Label(tab1, text="-", width=1)
    e_maxSize = Entry(tab1, width=5)
    s_methDur = Label(tab1, text="/", width=1)
    c_methDur = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_reverseChance = Label(tab1, text="Reverse chance: ")
    e_reverseChance = Entry(tab1, width=3)
    p_reverseChance = Label(tab1, text="%", width=2)

    l_PL = Label(tab1, text="Gap length: ")
    e_minPL = Entry(tab1, width=5)
    s_PL = Label(tab1, text="-", width=1)
    e_maxPL = Entry(tab1, width=5)
    s_methPause = Label(tab1, text="/", width=1)
    c_methPause = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_stopChance = Label(tab1, text="Chance to stop: ")
    e_stopChance = Entry(tab1, width=3)
    p_stopChance = Label(tab1, text="%", width=2)
    l_conspause = Label(tab1, text="Chance of consecutive pausing: ")
    e_conspause = Entry(tab1, width=3)
    p_conspause = Label(tab1, text="%", width=2)

    l_FadeIn = Label(tab1, text="Fade-in length: ")
    e_minFadeIn = Entry(tab1, width=5)
    s_FadeIn = Label(tab1, text="-", width=1)
    e_maxFadeIn = Entry(tab1, width=5)
    s_methFdIn = Label(tab1, text="/", width=1)
    c_methFdIn = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_fadeInChance = Label(tab1, text="Chance to fade-in: ")
    e_fadeInChance = Entry(tab1, width=3)
    p_fadeInChance = Label(tab1, text="%", width=2)

    l_FadeOut = Label(tab1, text="Fade-out length: ")
    e_minFadeOut = Entry(tab1, width=5)
    s_FadeOut = Label(tab1, text="-", width=1)
    e_maxFadeOut = Entry(tab1, width=5)
    s_methFdOut = Label(tab1, text="/", width=1)
    c_methFdOut = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_fadeOutChance = Label(tab1, text="Chance to fade-out: ")
    e_fadeOutChance = Entry(tab1, width=3)
    p_fadeOutChance = Label(tab1, text="%", width=2)

    l_fdprior = Label(tab1, text="Apply fades before reversal (chance): ")
    e_fdprior = Entry(tab1, width=3)
    p_fdprior = Label(tab1, text="%", width=2)
    l_faderestrict = Label(tab1, text="Fade only into pauses (chance): ")
    e_faderestrict = Entry(tab1, width=3)
    p_faderestrict = Label(tab1, text="%", width=2)

    l_crossfade = Label(tab1, text="Crossfade length: ")
    e_mincrossfade = Entry(tab1, width=5)
    s_crossfade = Label(tab1, text="-", width=1)
    e_maxcrossfade = Entry(tab1, width=5)
    s_methCrsfd = Label(tab1, text="/", width=1)
    c_methCrsfd = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_crossfadechance = Label(tab1, text="Chance to crossfade: ")
    e_crossfadechance = Entry(tab1, width=3)
    p_crossfadechance = Label(tab1, text="%", width=2)

    l_repeat = Label(tab1, text="Repeat segment ... times: ")
    e_repeatMin = Entry(tab1, width=5)
    s_repeat = Label(tab1, text="-", width=1)
    e_repeatMax = Entry(tab1, width=5)
    s_methrep = Label(tab1, text="/", width=1)
    c_methrep = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_repeatchance = Label(tab1, text="Chance to repeat: ")
    e_repeatchance = Entry(tab1, width=3)
    p_repeatchance = Label(tab1, text="%", width=2)
    l_consrep = Label(tab1, text="Chance of consecutive repeating: ")
    e_consrep = Entry(tab1, width=3)
    p_consrep = Label(tab1, text="%", width=2)

    l_remember = Label(tab1, text="Repeat after ... segments: ")
    e_minsegs = Entry(tab1, width=5)
    s_segs = Label(tab1, text="-", width=1)
    e_maxsegs = Entry(tab1, width=5)
    s_remembertype = Label(tab1, text="/", width=1)
    c_remembertype = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_rememberchance = Label(tab1, text="Chance to reappear: ")
    e_rememberchance = Entry(tab1, width=3)
    p_rememberchance = Label(tab1, text="%", width=2)

    l_avgstrt = Label(tab1, text="Average start times: ")
    e_avgstrt = Entry(tab1, width=33)
    l_strtdev = Label(tab1, text="Normal start deviation: ")
    e_strtdev = Entry(tab1, width=6)

    l_strtweights = Label(tab1, text="Start time weights: ")
    e_strtweights = Entry(tab1, width=33)
    l_normStrtChance = Label(tab1, text="Normal start chance: ")
    e_normStrtChance = Entry(tab1, width=3)
    p_normStrtChance = Label(tab1, text="%", width=2)

    l_speeds = Label(tab1, text="Speed variations: ")
    e_speeds = Entry(tab1, width=63)
    l_speedweights = Label(tab1, text="Variation weights: ")
    e_speedweights = Entry(tab1, width=63)

    l_TimeMeasure = Label(tab1, text="Time measure: ")
    c_TimeMeasure = Combobox(tab1, values=timemodes, width=60, state="readonly")
    l_fdmode = Label(tab1, text="Fade modes weights: ")
    l_fdmode_lc = Label(tab1, text="Lengthen chunks: ")
    e_fdmode_lc = Entry(tab1, width=6)
    l_fdmode_sf = Label(tab1, text="Shorten fades: ")
    e_fdmode_sf = Entry(tab1, width=6)
    l_fdmode_en = Label(tab1, text="Extend notes: ")
    e_fdmode_en = Entry(tab1, width=6)

    # Advanced tab
    adv_column1 = Frame(tab2)
    adv_column2 = Frame(tab2)
    adv_column3 = Frame(tab2)
    adv_column4 = Frame(tab2)

    lf_backmask = LabelFrame(adv_column1, text="Backmasking: ", padding=2)
    l_BackmaskCrossfade = Label(lf_backmask, text="Crossfade: ")
    e_BackmaskCrossfade = Entry(lf_backmask, width=5)
    lf_MaskChances = LabelFrame(lf_backmask, text="Chances: ", padding=2)
    l_BackmaskChance = Label(lf_MaskChances, text="Backmask (General): ")
    e_BackmaskChance = Entry(lf_MaskChances, width=3)
    p_BackmaskChance = Label(lf_MaskChances, text="%", width=2)
    l_asymmetricalBackmaskChance = Label(lf_MaskChances, text="Asymmetrical backmask: ")
    e_asymmetricalBackmaskChance = Entry(lf_MaskChances, width=3)
    p_asymmetricalBackmaskChance = Label(lf_MaskChances, text="%", width=2)
    l_reverseMaskChance = Label(lf_MaskChances, text="Reverse mask: ")
    e_reverseMaskChance = Entry(lf_MaskChances, width=3)
    p_reverseMaskChance = Label(lf_MaskChances, text="%", width=2)
    l_doublesize = Label(lf_MaskChances, text="Double segment size: ")
    e_doublesize = Entry(lf_MaskChances, width=3)
    p_doublesize = Label(lf_MaskChances, text="%", width=2)
    l_consecbackmask = Label(lf_MaskChances, text="Consecutive backmasking: ")
    e_consecbackmask = Entry(lf_MaskChances, width=3)
    p_consecbackmask = Label(lf_MaskChances, text="%", width=2)
    lf_MaskRepeat = LabelFrame(lf_backmask, text="Repeats: ", padding=2)
    l_minMaskRepeat = Label(lf_MaskRepeat, text="Minimum: ")
    e_minMaskRepeat = Entry(lf_MaskRepeat, width=4)
    l_maxMaskRepeat = Label(lf_MaskRepeat, text="Maximum: ")
    e_maxMaskRepeat = Entry(lf_MaskRepeat, width=4)
    l_methrepmsk = Label(lf_MaskRepeat, text="Method: ")
    c_methrepmsk = Combobox(lf_MaskRepeat, values=randmodes, width=14, state="readonly")
    l_maskmode = Label(lf_MaskRepeat, text="Measure: ")
    c_maskmode = Combobox(lf_MaskRepeat, values=repmeasmodes, width=14, state="readonly")
    l_maskRepeatChance = Label(lf_MaskRepeat, text="Chance: ")
    e_maskRepeatChance = Entry(lf_MaskRepeat, width=3)
    p_maskRepeatChance = Label(lf_MaskRepeat, text="%", width=2)

    lf_Stumbling = LabelFrame(adv_column2, text="Stumbling: ", padding=2)
    l_stumblechance = Label(lf_Stumbling, text="Stumble chance: ")
    e_stumblechance = Entry(lf_Stumbling, width=14)
    p_stumblechance = Label(lf_Stumbling, text="%")
    l_stumbledeviation = Label(lf_Stumbling, text="Stumble deviation: ")
    e_stumbledeviation = Entry(lf_Stumbling, width=17)
    l_methStumble = Label(lf_Stumbling, text="Stumbling method: ")
    c_methStumble = Combobox(lf_Stumbling, values=stumbmodes, width=14, state="readonly")
    l_stumavgstrt = Label(lf_Stumbling, text="Ignore average start times: ")
    e_stumavgstrt = Entry(lf_Stumbling, width=14)
    p_stumavgstrt = Label(lf_Stumbling, text="%")
    l_countstumblepauses = Label(lf_Stumbling, text="Count pauses: ")
    e_countstumblepauses = Entry(lf_Stumbling, width=14)
    p_countstumblepauses = Label(lf_Stumbling, text="%")

    x_notepropfd = IntVar()
    x_fromseed = IntVar()
    lf_Misc = LabelFrame(adv_column2, text="Misc: ", padding=2)
    l_propfadein = Label(lf_Misc, text="Measure (Fade-in length): ")
    c_propfadein = Combobox(lf_Misc, values=propfademodes, width=8, state="readonly")
    l_propfadeout = Label(lf_Misc, text="Measure (Fade-out length): ")
    c_propfadeout = Combobox(lf_Misc, values=propfademodes, width=8, state="readonly")
    l_repmode = Label(lf_Misc, text="Measure (Segment repeats): ")
    c_repmode = Combobox(lf_Misc, values=repmeasmodes, width=8, state="readonly")
    l_minfdmsk = Label(lf_Misc, text="Minimum fade backmask: ")
    e_minfdmsk = Entry(lf_Misc, width=11)
    c_notepropfd = Checkbutton(lf_Misc, text="Measure backmask fade from last note", variable=x_notepropfd)
    c_fromseed = Checkbutton(lf_Misc, text="Generate from seed: ", variable=x_fromseed, command=lambda: updateSymbols())
    e_seed = Entry(lf_Misc, width=11)

    lf_Quantization = LabelFrame(adv_column3, text="Quantization: ", padding=2)
    l_quantizeMode = Label(lf_Quantization, text="Mode: ")
    c_quantizeMode = Combobox(lf_Quantization, values=quantmodes, width=13, state="readonly")
    l_bpm = Label(lf_Quantization, text="BPM: ")
    e_bpm = Entry(lf_Quantization, width=16)
    lf_QuantizationChances = LabelFrame(lf_Quantization, text="Chances: ", padding=2)
    l_quanavgstrt = Label(lf_QuantizationChances, text="Average start times: ")
    e_quanavgstrt = Entry(lf_QuantizationChances, width=3)
    p_quanavgstrt = Label(lf_QuantizationChances, text="%")
    l_quanstrt = Label(lf_QuantizationChances, text="Start times: ")
    e_quanstrt = Entry(lf_QuantizationChances, width=3)
    p_quanstrt = Label(lf_QuantizationChances, text="%")
    l_quanseglgth = Label(lf_QuantizationChances, text="Segment length: ")
    e_quanseglgth = Entry(lf_QuantizationChances, width=3)
    p_quanseglgth = Label(lf_QuantizationChances, text="%")
    l_quanrep = Label(lf_QuantizationChances, text="Segment repeats: ")
    e_quanrep = Entry(lf_QuantizationChances, width=3)
    p_quanrep = Label(lf_QuantizationChances, text="%")
    l_quanmask = Label(lf_QuantizationChances, text="Mask repeats: ")
    e_quanmask = Entry(lf_QuantizationChances, width=3)
    p_quanmask = Label(lf_QuantizationChances, text="%")
    l_usestartonsets = Label(lf_QuantizationChances, text="Use start onsets: ")
    e_usestartonsets = Entry(lf_QuantizationChances, width=3)
    p_usestartonsets = Label(lf_QuantizationChances, text="%")
    b_onsets = Button(lf_Quantization, text="Manage onsets", command=lambda: run(abOnsetsWindow))

    x_trimfile = IntVar()
    x_shiftons = IntVar()
    lf_Trim = LabelFrame(adv_column4, text="Trim: ", padding=2)
    c_trimfile = Checkbutton(lf_Trim, text="Trim audio file", variable=x_trimfile, command=lambda: updateSymbols())
    l_trimmin = Label(lf_Trim, text="From: ")
    e_trimmin = Entry(lf_Trim, width=7)
    l_trimmax = Label(lf_Trim, text="To: ")
    e_trimmax = Entry(lf_Trim, width=7)
    c_shiftons = Checkbutton(lf_Trim, text="Shift onset times", variable=x_shiftons)

    # Main tab (grid)
    tab1_sep1.grid(row=0, column=6)
    tab1_sep2.grid(row=0, column=10)
    tab1_sep3.grid(row=0, column=11)
    tab1_sep4.grid(row=11, column=0)

    l_Size.grid(row=0, column=0, sticky="w")
    e_minSize.grid(row=0, column=1)
    s_Size.grid(row=0, column=2)
    e_maxSize.grid(row=0, column=3)
    s_methDur.grid(row=0, column=4)
    c_methDur.grid(row=0, column=5)
    l_reverseChance.grid(row=0, column=7, sticky="w")
    e_reverseChance.grid(row=0, column=8)
    p_reverseChance.grid(row=0, column=9)

    l_PL.grid(row=1, column=0, sticky="w")
    e_minPL.grid(row=1, column=1)
    s_PL.grid(row=1, column=2)
    e_maxPL.grid(row=1, column=3)
    s_methPause.grid(row=1, column=4)
    c_methPause.grid(row=1, column=5)
    l_stopChance.grid(row=1, column=7, sticky="w")
    e_stopChance.grid(row=1, column=8)
    p_stopChance.grid(row=1, column=9)
    l_conspause.grid(row=1, column=12, sticky="w")
    e_conspause.grid(row=1, column=13)
    p_conspause.grid(row=1, column=14)

    l_FadeIn.grid(row=2, column=0, sticky="w")
    e_minFadeIn.grid(row=2, column=1)
    s_FadeIn.grid(row=2, column=2)
    e_maxFadeIn.grid(row=2, column=3)
    s_methFdIn.grid(row=2, column=4)
    c_methFdIn.grid(row=2, column=5)
    l_fadeInChance.grid(row=2, column=7, sticky="w")
    e_fadeInChance.grid(row=2, column=8)
    p_fadeInChance.grid(row=2, column=9)

    l_FadeOut.grid(row=3, column=0, sticky="w")
    e_minFadeOut.grid(row=3, column=1)
    s_FadeOut.grid(row=3, column=2)
    e_maxFadeOut.grid(row=3, column=3)
    s_methFdOut.grid(row=3, column=4)
    c_methFdOut.grid(row=3, column=5)
    l_fadeOutChance.grid(row=3, column=7, sticky="w")
    e_fadeOutChance.grid(row=3, column=8)
    p_fadeOutChance.grid(row=3, column=9)

    l_fdprior.grid(row=2, column=12, sticky="w")
    e_fdprior.grid(row=2, column=13)
    p_fdprior.grid(row=2, column=14)
    l_faderestrict.grid(row=3, column=12, sticky="w")
    e_faderestrict.grid(row=3, column=13)
    p_faderestrict.grid(row=3, column=14)

    l_crossfade.grid(row=4, column=0, sticky="w")
    e_mincrossfade.grid(row=4, column=1)
    s_crossfade.grid(row=4, column=2)
    e_maxcrossfade.grid(row=4, column=3)
    s_methCrsfd.grid(row=4, column=4)
    c_methCrsfd.grid(row=4, column=5)
    l_crossfadechance.grid(row=4, column=7, sticky="w")
    e_crossfadechance.grid(row=4, column=8)
    p_crossfadechance.grid(row=4, column=9)

    l_repeat.grid(row=5, column=0, sticky="w")
    e_repeatMin.grid(row=5, column=1)
    s_repeat.grid(row=5, column=2)
    e_repeatMax.grid(row=5, column=3)
    s_methrep.grid(row=5, column=4)
    c_methrep.grid(row=5, column=5)
    l_repeatchance.grid(row=5, column=7, sticky="w")
    e_repeatchance.grid(row=5, column=8)
    p_repeatchance.grid(row=5, column=9)
    l_consrep.grid(row=5, column=12, sticky="w")
    e_consrep.grid(row=5, column=13)
    p_consrep.grid(row=5, column=14)

    l_remember.grid(row=6, column=0, sticky="w")
    e_minsegs.grid(row=6, column=1)
    s_segs.grid(row=6, column=2)
    e_maxsegs.grid(row=6, column=3)
    s_remembertype.grid(row=6, column=4)
    c_remembertype.grid(row=6, column=5)
    l_rememberchance.grid(row=6, column=7, sticky="w")
    e_rememberchance.grid(row=6, column=8)
    p_rememberchance.grid(row=6, column=9)

    l_avgstrt.grid(row=7, column=0, sticky="w")
    e_avgstrt.grid(row=7, column=1, columnspan=5)
    l_strtdev.grid(row=7, column=7, sticky="w")
    e_strtdev.grid(row=7, column=8, columnspan=2)

    l_strtweights.grid(row=8, column=0, sticky="w")
    e_strtweights.grid(row=8, column=1, columnspan=5)
    l_normStrtChance.grid(row=8, column=7, sticky="w")
    e_normStrtChance.grid(row=8, column=8)
    p_normStrtChance.grid(row=8, column=9)

    l_speeds.grid(row=9, column=0, sticky="w")
    e_speeds.grid(row=9, column=1, columnspan=9)
    l_speedweights.grid(row=10, column=0, sticky="w")
    e_speedweights.grid(row=10, column=1, columnspan=9)

    l_TimeMeasure.grid(row=12, column=0, sticky="w")
    c_TimeMeasure.grid(row=12, column=1, columnspan=9)
    l_fdmode.grid(row=13, column=0, sticky="w")
    l_fdmode_lc.grid(row=13, column=1, columnspan=7, sticky="w")
    e_fdmode_lc.grid(row=13, column=8, columnspan=2)
    l_fdmode_sf.grid(row=14, column=1, columnspan=7, sticky="w")
    e_fdmode_sf.grid(row=14, column=8, columnspan=2)
    l_fdmode_en.grid(row=15, column=1, columnspan=7, sticky="w")
    e_fdmode_en.grid(row=15, column=8, columnspan=2)

    # Advanced tab (grid)
    adv_column1.grid(row=0, column=0, sticky="n")
    adv_column2.grid(row=0, column=1, sticky="n")
    adv_column3.grid(row=0, column=2, sticky="n")
    adv_column4.grid(row=0, column=3, sticky="n")

    lf_backmask.grid(row=0, column=0, padx=3, sticky="n")
    l_BackmaskCrossfade.grid(row=0, column=0, sticky="w")
    e_BackmaskCrossfade.grid(row=0, column=1, sticky="e")
    lf_MaskChances.grid(row=1, column=0, columnspan=2)
    l_BackmaskChance.grid(row=0, column=0, sticky="w")
    e_BackmaskChance.grid(row=0, column=1)
    p_BackmaskChance.grid(row=0, column=2)
    l_asymmetricalBackmaskChance.grid(row=1, column=0, sticky="w")
    e_asymmetricalBackmaskChance.grid(row=1, column=1)
    p_asymmetricalBackmaskChance.grid(row=1, column=2)
    l_reverseMaskChance.grid(row=2, column=0, sticky="w")
    e_reverseMaskChance.grid(row=2, column=1)
    p_reverseMaskChance.grid(row=2, column=2)
    l_doublesize.grid(row=3, column=0, sticky="w")
    e_doublesize.grid(row=3, column=1)
    p_doublesize.grid(row=3, column=2)
    l_consecbackmask.grid(row=4, column=0, sticky="w")
    e_consecbackmask.grid(row=4, column=1)
    p_consecbackmask.grid(row=4, column=2)
    lf_MaskRepeat.grid(row=2, column=0, columnspan=2)
    l_minMaskRepeat.grid(row=0, column=0, sticky="w")
    e_minMaskRepeat.grid(row=0, column=1, sticky="e")
    l_maxMaskRepeat.grid(row=1, column=0, sticky="w")
    e_maxMaskRepeat.grid(row=1, column=1, sticky="e")
    l_methrepmsk.grid(row=2, column=0, sticky="w")
    c_methrepmsk.grid(row=2, column=1)
    l_maskmode.grid(row=3, column=0, sticky="w")
    c_maskmode.grid(row=3, column=1)
    l_maskRepeatChance.grid(row=4, column=0, sticky="w")
    e_maskRepeatChance.grid(row=4, column=1, sticky="e")
    p_maskRepeatChance.grid(row=4, column=2)

    lf_Stumbling.grid(row=0, column=0, padx=3, sticky="wn")
    l_stumblechance.grid(row=0, column=0, sticky="w")
    e_stumblechance.grid(row=0, column=1)
    p_stumblechance.grid(row=0, column=2)
    l_stumbledeviation.grid(row=1, column=0, sticky="w")
    e_stumbledeviation.grid(row=1, column=1, columnspan=2)
    l_methStumble.grid(row=2, column=0, sticky="w")
    c_methStumble.grid(row=2, column=1, columnspan=2)
    l_stumavgstrt.grid(row=3, column=0, sticky="w")
    e_stumavgstrt.grid(row=3, column=1)
    p_stumavgstrt.grid(row=3, column=2)
    l_countstumblepauses.grid(row=4, column=0, sticky="w")
    e_countstumblepauses.grid(row=4, column=1)
    p_countstumblepauses.grid(row=4, column=2)

    lf_Misc.grid(row=1, column=0, padx=3, sticky="wn")
    l_propfadein.grid(row=0, column=0, sticky="w")
    c_propfadein.grid(row=0, column=1, sticky="e")
    l_propfadeout.grid(row=1, column=0, sticky="w")
    c_propfadeout.grid(row=1, column=1, sticky="e")
    l_repmode.grid(row=2, column=0, sticky="w")
    c_repmode.grid(row=2, column=1, sticky="e")
    l_minfdmsk.grid(row=3, column=0, sticky="w")
    e_minfdmsk.grid(row=3, column=1, sticky="e")
    c_notepropfd.grid(row=4, column=0, sticky="w", columnspan=2)
    c_fromseed.grid(row=5, column=0, sticky="w")
    e_seed.grid(row=5, column=1, sticky="e")

    lf_Quantization.grid(row=0, column=0, padx=3, sticky="wn")
    l_quantizeMode.grid(row=0, column=0, sticky="w")
    c_quantizeMode.grid(row=0, column=1)
    l_bpm.grid(row=1, column=0, sticky="w")
    e_bpm.grid(row=1, column=1)
    lf_QuantizationChances.grid(row=2, column=0, columnspan=2)
    l_quanavgstrt.grid(row=0, column=0, sticky="w")
    e_quanavgstrt.grid(row=0, column=1)
    p_quanavgstrt.grid(row=0, column=2)
    l_quanstrt.grid(row=1, column=0, sticky="w")
    e_quanstrt.grid(row=1, column=1)
    p_quanstrt.grid(row=1, column=2)
    l_quanseglgth.grid(row=2, column=0, sticky="w")
    e_quanseglgth.grid(row=2, column=1)
    p_quanseglgth.grid(row=2, column=2)
    l_quanrep.grid(row=3, column=0, sticky="w")
    e_quanrep.grid(row=3, column=1)
    p_quanrep.grid(row=3, column=2)
    l_quanmask.grid(row=4, column=0, sticky="w")
    e_quanmask.grid(row=4, column=1)
    p_quanmask.grid(row=4, column=2)
    l_usestartonsets.grid(row=5, column=0, sticky="w")
    e_usestartonsets.grid(row=5, column=1)
    p_usestartonsets.grid(row=5, column=2)
    b_onsets.grid(row=3, column=0, columnspan=2)

    lf_Trim.grid(row=0, column=0, padx=3, sticky="wn")
    c_trimfile.grid(row=0, column=0, columnspan=2, sticky="w")
    l_trimmin.grid(row=1, column=0, sticky="w")
    e_trimmin.grid(row=1, column=1, sticky="e")
    l_trimmax.grid(row=2, column=0, sticky="w")
    e_trimmax.grid(row=2, column=1, sticky="e")
    c_shiftons.grid(row=3, column=0, columnspan=2, sticky="w")

    # Progress bar
    pbar = Frame(window)
    progress = Progressbar(pbar, orient="horizontal")
    b_abort = Button(pbar, text="Abort", state="disabled", command=lambda: genAbort())
    progress.pack(side="left", fill="x", expand=True)
    b_abort.pack(side="right")
    pbar.pack(side="bottom", fill="x", padx=pbpadx)

    # Combobox binds
    c_methDur.bind("<<ComboboxSelected>>", updateSymbols)
    c_methPause.bind("<<ComboboxSelected>>", updateSymbols)
    c_methFdIn.bind("<<ComboboxSelected>>", updateSymbols)
    c_methFdOut.bind("<<ComboboxSelected>>", updateSymbols)
    c_methCrsfd.bind("<<ComboboxSelected>>", updateSymbols)
    c_repmode.bind("<<ComboboxSelected>>", updateSymbols)
    c_methrep.bind("<<ComboboxSelected>>", updateSymbols)
    c_remembertype.bind("<<ComboboxSelected>>", updateSymbols)
    c_methrepmsk.bind("<<ComboboxSelected>>", updateSymbols)
    c_quantizeMode.bind("<<ComboboxSelected>>", updateSymbols)
    c_propfadein.bind("<<ComboboxSelected>>", updateSymbols)
    c_propfadeout.bind("<<ComboboxSelected>>", updateSymbols)

    # Hotkey binds
    window.bind("<Control-i>", lambda event: run(genImportAudio))
    window.bind("<Control-Shift-I>", lambda event: run(genImportAudio, False, True))
    window.bind("<Control-e>", lambda event: run(genScramble, True, getExportLength()))
    window.bind("<Control-r>", lambda event: run(genImportAudio, True))
    window.bind("<Control-o>", lambda event: cfgImport())
    window.bind("<Control-s>", lambda event: cfgExport())
    window.bind("<Control-n>", lambda event: abDefaultConfig())
    if not AB_DISABLE_SIMPLEAUDIO:
        window.bind("<Control-p>", lambda event: run(genScramble, False, stp.get()))
        window.bind("<Control-Alt-p>", lambda event: genStopPreview())

    # Configure
    useunixfilename.set(binBool(abConfig.get("useunixfilename")))
    secimpaudlen.set(binBool(abConfig.get("secimpaudlen")))
    shadderrinf.set(binBool(abConfig.get("shadderrinf")))
    autoonsdet.set(binBool(abConfig.get("autoonsdet")))
    resetonsets.set(binBool(abConfig.get("resetonsets")))
    closeonsets.set(binBool(abConfig.get("closeonsets")))
    if AB_DISABLE_LIBROSA: autoonsdet.set(0)

    updateWindow()
    applyWindowStyle(window)
    abDefaultConfig()
    window.mainloop()
    sys.exit()
