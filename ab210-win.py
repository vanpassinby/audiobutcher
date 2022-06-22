import os
import time
import pydub
import base64
import random
import pathlib
import pyaudio
import threading
import webbrowser
import configparser
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter.ttk import Combobox
import tkinter.simpledialog as sd
from tkinter.simpledialog import askinteger
from pydub.playback import play
from pydub import AudioSegment

pathsrcaud = ""
pathresaud = ""
pathtopreset = ""
importstate = "none"
segTime = 0
gen_good = 0

randmodes = ("Uniform", "Normal", "Lognormal")
randmodes_rep = ("Uniform", "Normal")
compmodes = ("Lengthen chunks", "Shorten fades")
stumbmodes = ("Standard", "Forwards only")
timemodes = ("Milliseconds (Note: start times are still in seconds)", "Seconds")

import_types = [("All supported formats", ("*.wav", "*.mp1", "*.mp2", "*.mp3", "*.ogg", "*.opus", "*.aif", "*.aiff", "*.aifc", "*.m4r", "*.au", "*.flac", "*.m4a", "*.gsm", "*.mpc", "*.ape")),
                ("Wave (*.wav)", "*.wav"),
                ("MPEG Layer-1 (*.mp1)", "*.mp1"),
                ("MPEG Layer-2 (*.mp2)", "*.mp2"),
                ("MPEG Layer-3 (*.mp3)", "*.mp3"),
                ("Ogg Vorbis (*.ogg)", "*.ogg"),
                ("Opus (*.opus)", "*.opus"),
                ("Apple AIFF (*.aif;*.aiff;*.aifc)", ("*.aif", "*.aiff", "*.aifc")),
                ("iPhone Ringtone (*.m4r)", "*.m4r"),
                ("Sun AU (*.au)", "*.au"),
                ("FLAC (*.flac)", "*.flac"),
                ("MPEG-4 Audio (*.m4a)", "*.m4a"),
                ("GSM (*.gsm)", "*.gsm"),
                ("AMR Narrowband Audio (*.amr)", "*.amr"),
                ("Musepack Audio (*.mpc)", "*.mpc"),
                ("Monkey's Audio Codec (*.ape)", "*.ape"),
                ("All files (*.*) ", "*.*")]

export_types = [("Wave (*.wav)", "*.wav"),
                ("MPEG Layer-3 (*.mp3)", "*.mp3"),
                ("FLAC (*.flac)", "*.flac"),
                ("Ogg Vorbis (*.ogg)", "*.ogg"),
                ("Apple AIFF (*.aiff)", "*.aiff"),
                ("Sun AU (*.au)", "*.au")]

preset_types = [("AudioButcher Preset (*.abp)", "*.abp"), ("All files (*.*)", "*.*")]

userprofile = os.environ['USERPROFILE']
windir = os.environ['WINDIR']
ABConfigPath = userprofile + "\\.audiobutcher"
ABConfig = configparser.RawConfigParser()

def license_window():
    lic = """
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
    
    licwin = Toplevel()
    licwin.title("License")
    licwin.geometry("640x480")
    licwin.resizable(width=False, height=False)
    licwin.iconphoto(False, PhotoImage(file=icon_file_path))
    
    scrollbar = Scrollbar(licwin)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    lictext = Text(licwin, yscrollcommand=scrollbar.set, wrap=WORD, width=65536, height=65536)
    lictext.insert(END, lic)
    lictext.configure(state=DISABLED)
    lictext.pack()
    scrollbar.config(command=lictext.yview)
    
    licwin.mainloop()

def seticon():
    global icon_file_path
    icon_b64 = b"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"
    icon_file_path = userprofile + "/AppData/Local/Temp/ab-icon.png"
    icon_file = open(icon_file_path, 'wb')
    icon_file.truncate(0)
    icon_file.seek(0)
    icon_file.write(bytes(base64.b64decode(icon_b64)))
    icon_file.close()
    window.iconphoto(False, PhotoImage(file=icon_file_path))

def getformat(name):
    fileformat = name.split(".")[-1]
    if fileformat=="aif": fileformat="aiff"
    if fileformat=="aifc": fileformat="aiff"
    return fileformat

def defaultpaths(mode, what):
    global pathsrcaud_default
    global pathresaud_default
    global pathtopreset_default
    ABConfig.read(ABConfigPath)
    if mode=="get":
        return ABConfig.get("AudioButcher_Path", what, fallback=userprofile)
    if mode=="set":
        pathsrcaud_default_new = defaultpaths("get", "pathsrcaud_default")
        pathresaud_default_new = defaultpaths("get", "pathresaud_default")
        pathtopreset_default_new = defaultpaths("get", "pathtopreset_default")
        if what=="pathsrcaud_default": pathsrcaud_default_new = pathlib.Path(pathsrcaud).parent.absolute()
        if what=="pathresaud_default": pathresaud_default_new = pathlib.Path(pathresaud).parent.absolute()
        if what=="pathtopreset_default": pathtopreset_default_new = pathlib.Path(pathtopreset).parent.absolute()
        cfgfile = open(ABConfigPath, 'w')
        cfgfile.truncate(0)
        cfgfile.seek(0)
        cfgfile.write("[AudioButcher_Path]\n")
        cfgfile.write("pathsrcaud_default = " + str(pathsrcaud_default_new) + "\n")
        cfgfile.write("pathresaud_default = " + str(pathresaud_default_new) + "\n")
        cfgfile.write("pathtopreset_default = " + str(pathtopreset_default_new) + "\n")
        cfgfile.close()

def mode2sym(mode):
    sym = ""
    if mode==0: sym="-"
    if mode==1: sym="±"
    if mode==2: sym=","
    return sym

def updatesym(dum):
    if c_methDur.current()==0 or c_methDur.current()==1:
        s_Size.config(text=mode2sym(c_methDur.current()))
        l_Size.config(text="Segment length: ")
    if c_methPause.current()==0 or c_methPause.current()==1:
        s_PL.config(text=mode2sym(c_methPause.current()))
        l_PL.config(text="Gap length: ")
    if c_methFdIn.current()==0 or c_methFdIn.current()==1:
        s_FadeIn.config(text=mode2sym(c_methFdIn.current()))
        l_FadeIn.config(text="Fade-in length: ")
    if c_methFdOut.current()==0 or c_methFdOut.current()==1:
        s_FadeOut.config(text=mode2sym(c_methFdOut.current()))
        l_FadeOut.config(text="Fade-out length: ")
    if c_methCrsfd.current()==0 or c_methCrsfd.current()==1:
        s_crossfade.config(text=mode2sym(c_methCrsfd.current()))
        l_crossfade.config(text="Crossfade length: ")
    s_repeat.config(text=mode2sym(c_methrep.current()))
    s_MaskRepeat.config(text=mode2sym(c_methrepmsk.current()))

    if c_methDur.current()==2: 
        l_Size.config(text="Segment length (µ, σ): ")
        s_Size.config(text=",")
    if c_methPause.current()==2: 
        l_PL.config(text="Gap length (µ, σ): ")
        s_PL.config(text=",")
    if c_methFdIn.current()==2:
        l_FadeIn.config(text="Fade-in length (µ, σ): ")
        s_FadeIn.config(text=",")
    if c_methFdOut.current()==2:
        l_FadeOut.config(text="Fade-out length (µ, σ): ")
        s_FadeOut.config(text=",")
    if c_methCrsfd.current()==2:
        l_crossfade.config(text="Crossfade length (µ, σ): ")
        s_crossfade.config(text=",")

def speed_change(sound, speed=0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * (2**(speed/12)))})
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def gen_main():
    global slicecr
    global gen_good
    
    gen_good = 0

    global audio
    lengthOfAudio = audio.duration_seconds*1000
    slicecr = AudioSegment.silent(duration = 1) #make slicecr audio that we can work with
    
    counter = 0
    firstTime = 1
    stumblestrt = 0
    
    if stumblechance > 0:
        audio += audio[0:0.1*lengthOfAudio]  #1.1x audio length to help prevent stumbling over file end
        newaudlgth = audio.duration_seconds*1000
    
    paused = 0
    repeated = 0
    
    while slicecr.duration_seconds < segTime:
        chance = random.uniform(0,100)
        inchance = random.uniform(0,100)
        outchance = random.uniform(0,100)
        crosschance = random.uniform(0,100)
        revchance = random.uniform(0,100)
        bkmskchance = random.uniform(0,100)
        repchance = random.uniform(0,100)
        nrmSrtChnce = random.uniform(0,100)
        stumbchnce = random.uniform(0,100)
        asymmaskchnce = random.uniform(0,100)
    
        startpool = random.choices(avgstrt,weights=strtweights,k=1)
        averagestart = random.choice(startpool)
    
        if nrmSrtChnce <= normStrtChance:
            startPosition = random.gauss(averagestart*1000,strtdev*1000)
            while startPosition < 0 or startPosition >= lengthOfAudio:
                startPosition = random.gauss(averagestart*1000,strtdev*1000)
        else:
            startPosition = random.uniform(0,lengthOfAudio)
    
    
        if crosschance <= crossfadechance:
            if methCrsfd == 0:
                crossfade = random.randint(mincrossfade,maxcrossfade)
            elif methCrsfd == 1:
                crossfade = int(abs(random.gauss(mincrossfade,maxcrossfade)))
            else:
                crossfade = int(random.lognormvariate(mincrossfade,maxcrossfade))
    
        else:
            crossfade = 0
    
        if firstTime == 1:                                      #check if it's first loop
            slicecr = AudioSegment.silent(duration = crossfade) #make silence length equal crossfade
            slicecr = slicecr.set_frame_rate(audio.frame_rate)  #defaults to 11025 for some reason. set to track rate.
            firstTime = 0
    
    
        if methDur == 0:
            randdur = random.uniform(minSize,maxSize)
        elif methDur == 1:
            randdur = abs(random.gauss(minSize,maxSize))
        else:
            randdur = random.lognormvariate(minSize,maxSize)
    
        if bkmskchance <= BackmaskChance and doublesize == 1:
            randdur *= 2
    
        randdur += crossfade
        
        if lengthOfAudio - startPosition < randdur:
            startPosition = lengthOfAudio - randdur
    
        if methPause == 0:
            pause = random.uniform(minPL,maxPL)
        elif methPause == 1:
            pause = abs(random.gauss(minPL,maxPL))
        else:
            pause = random.lognormvariate(minPL,maxPL)
    
        pause += crossfade
    
        if inchance <= fadeInChance:
            if methFdIn == 0:
                fadein = random.randint(minFadeIn,maxFadeIn)
            elif methFdIn == 1:
                fadein = int(abs(random.gauss(minFadeIn,maxFadeIn)))
            else:
                fadein = int(random.lognormvariate(minFadeIn,maxFadeIn))
        else:
            fadein = 0
        
        if outchance <= fadeOutChance:
            if methFdOut == 0:
                fadeout = random.randint(minFadeOut,maxFadeOut)
            elif methFdOut == 1:
                fadeout = int(abs(random.gauss(minFadeOut,maxFadeOut)))
            else:
                fadeout = int(random.lognormvariate(minFadeOut,maxFadeOut))
        else:
            fadeout = 0
        
        if randdur < fadein + fadeout: #if possible fade times are longer than duration, increase duration to fade times
            if CompMethod == 0:
                randdur = fadein + fadeout + crossfade
            else:
                if fadein > randdur/2:
                    fadein = int(randdur/2)
                if fadeout > randdur/2:
                    fadeout = int(randdur/2)
    
        if methrep == 0:
            repeatcounter = random.randint(repeatMin,repeatMax)
        elif methrep == 1:
            repeatcounter = -1
            while repeatcounter < 0:
                repeatcounter = random.gauss(repeatMin,repeatMax)
                if repeatcounter < 1 and repeatcounter > 0:
                    repeatcounter = 1
                repeatcounter = int(repeatcounter)
    
        if methrepmsk == 0:
            maskrepeatcounter = random.randint(minMaskRepeat,maxMaskRepeat)
        elif methrepmsk == 1:
            maskrepeatcounter = -1
            while maskrepeatcounter < 0:
                maskrepeatcounter = random.gauss(minMaskRepeat,maxMaskRepeat)
                if maskrepeatcounter < 1 and maskrepeatcounter > 0:
                    maskrepeatcounter = 1
                maskrepeatcounter = int(maskrepeatcounter)
    
    
        speedgrab = random.choices(speeds,weights=speedweights,k=1)
        speed = random.choice(speedgrab)
    
        #append
        
        if stumbchnce <= stumblechance:
            if methStumble == 0:
                startPosition = abs(random.gauss(stumblestrt,stumbledeviation))
            elif methStumble == 1:
                startPosition = stumblestrt + abs(random.gauss(0,stumbledeviation))

        if stumblechance > 0:
            if newaudlgth - startPosition < randdur:
                startPosition = newaudlgth - randdur


        if chance < (100 - stopChance) or paused == 1:
        
            appender = audio[startPosition:startPosition + randdur * (audio.frame_rate * (2**(speed/12))/audio.frame_rate)]    #get audio segment, apply speed change if neccesary
    
            #apply reverse if applicable
            if revchance <= reverseChance and not(bkmskchance <= BackmaskChance):
                appender = appender.reverse()
                if appender.channels == 2:
                    appender = appender.split_to_mono()        #reversing switches channels for some reason
                    appender = AudioSegment.from_mono_audiosegments(appender[1], appender[0])
    
            #apply speed change
            appender = speed_change(appender,speed)
    
            #backmasking
            if bkmskchance <= BackmaskChance:
                bckmskfde = BackmaskCrossfade
                if asymmaskchnce >= asymmetricalBackmaskChance:
                    
                    appender = appender[0:randdur/2]
    
                    if revchance <= reverseMaskChance:
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
                        while maskrepeatcounter > 0:
                            appender = appender.append(temppender, crossfade=bckmskfde)
                            maskrepeatcounter -= 1
    
                else:
                    appendlength = appender.duration_seconds*1000
    
                    if revchance <= reverseMaskChance:
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
    
    
            #apply fades
            if fadein > 0:
                appender = appender.fade_in(fadein)
            if fadeout > 0:
                appender = appender.fade_out(fadeout)
    
    
            paused = 0
        else:
            #add silence to file
            appender = AudioSegment.silent(duration=pause)
            if conspause == 0:
                paused = 1
    
    
        if repchance <= repeatchance and repeated == 0 and not(bkmskchance <= BackmaskChance and (asymmaskchnce >= asymmetricalBackmaskChance)):
            while repeatcounter >= 0:
                if methStumble == 0:
                    stumblestrt += (appender.duration_seconds*1000 - crossfade) * (audio.frame_rate * (2**(speed/12))/audio.frame_rate)
                elif methStumble == 1:
                    stumblestrt = startPosition + (appender.duration_seconds*1000 - crossfade) * (audio.frame_rate * (2**(speed/12))/audio.frame_rate)
    
                if stumblestrt > lengthOfAudio:
                    stumblestrt = stumblestrt - lengthOfAudio
    
    
                #append segment to final variable
                slicecr = slicecr.append(appender, crossfade=crossfade)
    
                #debug second/segment counter
                counter +=1
                progress['value']=slicecr.duration_seconds/segTime*100
                repeatcounter -= 1
            if consrep == 0:
                repeated = 1
        else:
            if methStumble == 0:
                stumblestrt += (appender.duration_seconds*1000 - crossfade) * (audio.frame_rate * (2**(speed/12))/audio.frame_rate)
            elif methStumble == 1:
                stumblestrt = startPosition + (appender.duration_seconds*1000 - crossfade) * (audio.frame_rate * (2**(speed/12))/audio.frame_rate)
    
            if stumblestrt > lengthOfAudio:
                stumblestrt = stumblestrt - lengthOfAudio
    
            if crossfade > appender.duration_seconds*1000:
                crossfade = int(appender.duration_seconds*1000)
                #print("crossfade shortened")
    
            #append segment to final variable
            slicecr = slicecr.append(appender, crossfade=crossfade)
    
            #debug second/segment counter
            counter +=1
            progress['value']=slicecr.duration_seconds/segTime*100
            repeated = 0
            
    gen_good = 1
    return slicecr

def config_empty():
    e_avgstrt.delete(0, END)
    e_strtweights.delete(0, END)
    e_strtdev.delete(0, END)
    e_normStrtChance.delete(0, END)
    e_stumblechance.delete(0, END)
    c_methStumble.current(0)
    e_stumbledeviation.delete(0, END)
    e_minSize.delete(0, END)
    e_maxSize.delete(0, END)
    c_methDur.current(0)
    e_minPL.delete(0, END)
    e_maxPL.delete(0, END)
    c_methPause.current(0)
    e_stopChance.delete(0, END)
    x_conspause.set(0)
    e_reverseChance.delete(0, END)
    e_BackmaskCrossfade.delete(0, END)
    e_BackmaskChance.delete(0, END)
    e_reverseMaskChance.delete(0, END)
    e_asymmetricalBackmaskChance.delete(0, END)
    x_doublesize.set(0)
    e_maskRepeatChance.delete(0, END)
    e_minMaskRepeat.delete(0, END)
    e_maxMaskRepeat.delete(0, END)
    c_methrepmsk.current(0)
    e_repeatchance.delete(0, END)
    e_repeatMin.delete(0, END)
    e_repeatMax.delete(0, END)
    c_methrep.current(0)
    x_consrep.set(0)
    e_mincrossfade.delete(0, END)
    e_maxcrossfade.delete(0, END)
    c_methCrsfd.current(0)
    e_crossfadechance.delete(0, END)
    e_minFadeIn.delete(0, END)
    e_maxFadeIn.delete(0, END)
    c_methFdIn.current(0)
    e_fadeInChance.delete(0, END)
    e_minFadeOut.delete(0, END)
    e_maxFadeOut.delete(0, END)
    c_methFdOut.current(0)
    e_fadeOutChance.delete(0, END)
    c_CompMethod.current(0)
    e_speeds.delete(0, END)
    e_speedweights.delete(0, END)
    c_TimeMeasure.current(0)

def config_default():
    e_avgstrt.insert(0, "0")
    e_strtweights.insert(0, "1")
    e_strtdev.insert(0, "0")
    e_normStrtChance.insert(0, "0")
    e_stumblechance.insert(0, "0")
    c_methStumble.current(0)
    e_stumbledeviation.insert(0, "0")
    e_minSize.insert(0, "0")
    e_maxSize.insert(0, "0")
    c_methDur.current(0)
    e_minPL.insert(0, "0")
    e_maxPL.insert(0, "0")
    c_methPause.current(0)
    e_stopChance.insert(0, "0")
    x_conspause.set(0)
    e_reverseChance.insert(0, "0")
    e_BackmaskCrossfade.insert(0, "0")
    e_BackmaskChance.insert(0, "0")
    e_reverseMaskChance.insert(0, "0")
    e_asymmetricalBackmaskChance.insert(0, "0")
    x_doublesize.set(0)
    e_maskRepeatChance.insert(0, "0")
    e_minMaskRepeat.insert(0, "0")
    e_maxMaskRepeat.insert(0, "0")
    c_methrepmsk.current(0)
    e_repeatchance.insert(0,"0")
    e_repeatMin.insert(0, "0")
    e_repeatMax.insert(0, "0")
    c_methrep.current(0)
    x_consrep.set(0)
    e_mincrossfade.insert(0, "0")
    e_maxcrossfade.insert(0, "0")
    c_methCrsfd.current(0)
    e_crossfadechance.insert(0, "100")
    e_minFadeIn.insert(0, "0")
    e_maxFadeIn.insert(0, "0")
    c_methFdIn.current(0)
    e_fadeInChance.insert(0, "100")
    e_minFadeOut.insert(0, "0")
    e_maxFadeOut.insert(0, "0")
    c_methFdOut.current(0)
    e_fadeOutChance.insert(0, "100")
    c_CompMethod.current(0)
    e_speeds.insert(0, "0")
    e_speedweights.insert(0, "1")
    c_TimeMeasure.current(0)

def config_apply():
    global avgstrt
    global strtweights
    global strtdev
    global normStrtChance
    global stumblechance
    global methStumble
    global stumbledeviation
    global minSize
    global maxSize
    global methDur
    global minPL
    global maxPL
    global methPause
    global stopChance
    global conspause
    global reverseChance
    global BackmaskChance
    global BackmaskCrossfade
    global reverseMaskChance
    global asymmetricalBackmaskChance
    global doublesize
    global maskRepeatChance
    global minMaskRepeat
    global maxMaskRepeat
    global methrepmsk
    global repeatchance
    global repeatMin
    global repeatMax
    global methrep
    global consrep
    global mincrossfade
    global maxcrossfade
    global methCrsfd
    global crossfadechance
    global minFadeIn
    global maxFadeIn
    global methFdIn
    global fadeInChance
    global minFadeOut
    global maxFadeOut
    global methFdOut
    global fadeOutChance
    global CompMethod
    global speeds
    global speedweights
    avgstrt = list(map(float, e_avgstrt.get().split(' ')))
    strtweights = list(map(int, e_strtweights.get().split(' ')))
    strtdev = float(e_strtdev.get())
    normStrtChance = float(e_normStrtChance.get())
    stumblechance = float(e_stumblechance.get())
    methStumble = c_methStumble.current()
    stumbledeviation = float(e_stumbledeviation.get())
    minSize = float(e_minSize.get())
    maxSize = float(e_maxSize.get())
    methDur = c_methDur.current()
    minPL = float(e_minPL.get())
    maxPL = float(e_maxPL.get())
    methPause = c_methPause.current()
    stopChance = float(e_stopChance.get())
    conspause = x_conspause.get()
    reverseChance = float(e_reverseChance.get())
    BackmaskChance = float(e_BackmaskChance.get())
    BackmaskCrossfade = int(float(e_BackmaskCrossfade.get()))
    reverseMaskChance = int(float(e_reverseMaskChance.get()))
    asymmetricalBackmaskChance = float(e_asymmetricalBackmaskChance.get())
    doublesize = x_doublesize.get()
    maskRepeatChance = float(e_maskRepeatChance.get())
    minMaskRepeat = int(float(e_minMaskRepeat.get()))
    maxMaskRepeat = int(float(e_maxMaskRepeat.get()))
    methrepmsk = c_methrepmsk.current()
    repeatchance = float(e_repeatchance.get())
    repeatMin = int(float(e_repeatMin.get()))
    repeatMax = int(float(e_repeatMax.get()))
    methrep = c_methrep.current()
    consrep = x_consrep.get()
    mincrossfade = int(float(e_mincrossfade.get()))
    maxcrossfade = int(float(e_maxcrossfade.get()))
    methCrsfd = c_methCrsfd.current()
    crossfadechance = float(e_crossfadechance.get())
    minFadeIn = int(float(e_minFadeIn.get()))
    maxFadeIn = int(float(e_maxFadeIn.get()))
    methFdIn = c_methFdIn.current()
    fadeInChance = float(e_fadeInChance.get())
    minFadeOut = int(float(e_minFadeOut.get()))
    maxFadeOut = int(float(e_maxFadeOut.get()))
    methFdOut = c_methFdOut.current()
    fadeOutChance = float(e_fadeOutChance.get())
    CompMethod = c_CompMethod.current()
    speeds = list(map(float, e_speeds.get().split(' ')))
    speedweights = list(map(int, e_speedweights.get().split(' ')))
    TimeMeasure = c_TimeMeasure.current()
    if TimeMeasure == 1:
        stumbledeviation*=1000
        BackmaskCrossfade*=1000
        if methDur!=2:
            minSize*=1000
            maxSize*=1000
        if methPause!=2:
            minPL*=1000
            maxPL*=1000
        if methCrsfd!=2:
            mincrossfade*=1000
            maxcrossfade*=1000
        if methFdIn!=2:
            minFadeIn*=1000
            maxFadeIn*=1000
        if methFdOut!=2:
            minFadeOut*=1000
            maxFadeOut*=1000

def config_import():
    global pathtopreset
    pathtopreset = fd.askopenfilename(filetypes=preset_types, defaultextension=preset_types, initialdir=defaultpaths("get", "pathtopreset_default"))
    if pathtopreset != "":
        defaultpaths("set", "pathtopreset_default")
        preset = configparser.RawConfigParser()
        preset.read(pathtopreset)
        config_empty()
        e_avgstrt.insert(0, preset.get("AudioButcher", "avgstrt", fallback="0"))
        e_strtweights.insert(0, preset.get("AudioButcher", "strtweights", fallback="1"))
        e_strtdev.insert(0, preset.get("AudioButcher", "strtdev", fallback="0"))
        e_normStrtChance.insert(0, preset.get("AudioButcher", "normStrtChance", fallback="0"))
        e_stumblechance.insert(0, preset.get("AudioButcher", "stumblechance", fallback="0"))
        c_methStumble.current(int(preset.get("AudioButcher", "methStumble", fallback="0")))
        e_stumbledeviation.insert(0, preset.get("AudioButcher", "stumbledeviation", fallback="0"))
        e_minSize.insert(0, preset.get("AudioButcher", "minSize", fallback="0"))
        e_maxSize.insert(0, preset.get("AudioButcher", "maxSize", fallback="0"))
        c_methDur.current(int(preset.get("AudioButcher", "methDur", fallback="0")))
        e_minPL.insert(0, preset.get("AudioButcher", "minPL", fallback="0"))
        e_maxPL.insert(0, preset.get("AudioButcher", "maxPL", fallback="0"))
        c_methPause.current(int(preset.get("AudioButcher", "methPause", fallback="0")))
        e_stopChance.insert(0, preset.get("AudioButcher", "stopChance", fallback="0"))
        x_conspause.set(int(preset.get("AudioButcher", "conspause", fallback="0")))
        e_reverseChance.insert(0, preset.get("AudioButcher", "reverseChance", fallback="0"))
        e_BackmaskCrossfade.insert(0, preset.get("AudioButcher", "BackmaskCrossfade", fallback="0"))
        e_BackmaskChance.insert(0, preset.get("AudioButcher", "BackmaskChance", fallback="0"))
        e_reverseMaskChance.insert(0, preset.get("AudioButcher", "reverseMaskChance", fallback="0"))
        e_asymmetricalBackmaskChance.insert(0, preset.get("AudioButcher", "asymmetricalBackmaskChance", fallback="0"))
        x_doublesize.set(int(preset.get("AudioButcher", "doublesize", fallback="0")))
        e_maskRepeatChance.insert(0, preset.get("AudioButcher", "maskRepeatChance", fallback="0"))
        e_minMaskRepeat.insert(0, preset.get("AudioButcher", "minMaskRepeat", fallback="0"))
        e_maxMaskRepeat.insert(0, preset.get("AudioButcher", "maxMaskRepeat", fallback="0"))
        c_methrepmsk.current(int(preset.get("AudioButcher", "methrepmsk", fallback="0")))
        e_repeatchance.insert(0, preset.get("AudioButcher", "repeatchance", fallback="0"))
        e_repeatMin.insert(0, preset.get("AudioButcher", "repeatMin", fallback="0"))
        e_repeatMax.insert(0, preset.get("AudioButcher", "repeatMax", fallback="0"))
        c_methrep.current(int(preset.get("AudioButcher", "methrep", fallback="0")))
        x_consrep.set(int(preset.get("AudioButcher", "consrep", fallback="0")))
        e_mincrossfade.insert(0, preset.get("AudioButcher", "mincrossfade", fallback="0"))
        e_maxcrossfade.insert(0, preset.get("AudioButcher", "maxcrossfade", fallback="0"))
        c_methCrsfd.current(int(preset.get("AudioButcher", "methCrsfd", fallback="0")))
        e_crossfadechance.insert(0, preset.get("AudioButcher", "crossfadechance", fallback="0"))
        e_minFadeIn.insert(0, preset.get("AudioButcher", "minFadeIn", fallback="0"))
        e_maxFadeIn.insert(0, preset.get("AudioButcher", "maxFadeIn", fallback="0"))
        c_methFdIn.current(int(preset.get("AudioButcher", "methFdIn", fallback="0")))
        e_fadeInChance.insert(0, preset.get("AudioButcher", "fadeInChance", fallback="0"))
        e_minFadeOut.insert(0, preset.get("AudioButcher", "minFadeOut", fallback="0"))
        e_maxFadeOut.insert(0, preset.get("AudioButcher", "maxFadeOut", fallback="0"))
        c_methFdOut.current(int(preset.get("AudioButcher", "methFdOut", fallback="0")))
        e_fadeOutChance.insert(0, preset.get("AudioButcher", "fadeOutChance", fallback="0"))
        c_CompMethod.current(int(preset.get("AudioButcher", "CompMethod", fallback="0")))
        e_speeds.insert(0, preset.get("AudioButcher", "speeds", fallback="0"))
        e_speedweights.insert(0, preset.get("AudioButcher", "speedweights", fallback="1"))
        c_TimeMeasure.current(int(preset.get("AudioButcher", "TimeMeasure", fallback="0")))
        updatesym(0)

def config_export():
    global pathtopreset
    pathtopreset = fd.asksaveasfilename(filetypes=preset_types, defaultextension=preset_types, initialdir=defaultpaths("get", "pathtopreset_default"))
    if pathtopreset!="": defaultpaths("set", "pathtopreset_default")
    if pathtopreset=="": pathtopreset="C:/nul"
    preset = open(pathtopreset, 'w')
    preset.truncate(0)
    preset.seek(0)
    preset.write("[AudioButcher]\n")
    preset.write("avgstrt = " + str(e_avgstrt.get()) + "\n")
    preset.write("strtweights = " + str(e_strtweights.get()) + "\n")
    preset.write("strtdev = " + str(e_strtdev.get()) + "\n")
    preset.write("normStrtChance = " + str(e_normStrtChance.get()) + "\n")
    preset.write("stumblechance = " + str(e_stumblechance.get()) + "\n")
    preset.write("methStumble = " + str(c_methStumble.current()) + "\n")
    preset.write("stumbledeviation = " + str(e_stumbledeviation.get()) + "\n")
    preset.write("minSize = " + str(e_minSize.get()) + "\n")
    preset.write("maxSize = " + str(e_maxSize.get()) + "\n")
    preset.write("methDur = " + str(c_methDur.current()) + "\n")
    preset.write("minPL = " + str(e_minPL.get()) + "\n")
    preset.write("maxPL = " + str(e_maxPL.get()) + "\n")
    preset.write("methPause = " + str(c_methPause.current()) + "\n")
    preset.write("stopChance = " + str(e_stopChance.get()) + "\n")
    preset.write("conspause = " + str(x_conspause.get()) + "\n")
    preset.write("reverseChance = " + str(e_reverseChance.get()) + "\n")
    preset.write("BackmaskCrossfade = " + str(e_BackmaskCrossfade.get()) + "\n")
    preset.write("BackmaskChance = " + str(e_BackmaskChance.get()) + "\n")
    preset.write("reverseMaskChance = " + str(e_reverseMaskChance.get()) + "\n")
    preset.write("asymmetricalBackmaskChance = " + str(e_asymmetricalBackmaskChance.get()) + "\n")
    preset.write("doublesize = " + str(x_doublesize.get()) + "\n")
    preset.write("maskRepeatChance = " + str(e_maskRepeatChance.get()) + "\n")
    preset.write("minMaskRepeat = " + str(e_minMaskRepeat.get()) + "\n")
    preset.write("maxMaskRepeat = " + str(e_maxMaskRepeat.get()) + "\n")
    preset.write("methrepmsk = " + str(c_methrepmsk.current()) + "\n")
    preset.write("repeatchance = " + str(e_repeatchance.get()) + "\n")
    preset.write("repeatMin = " + str(e_repeatMin.get()) + "\n")
    preset.write("repeatMax = " + str(e_repeatMax.get()) + "\n")
    preset.write("methrep = " + str(c_methrep.current()) + "\n")
    preset.write("consrep = " + str(x_consrep.get()) + "\n")
    preset.write("mincrossfade = " + str(e_mincrossfade.get()) + "\n")
    preset.write("maxcrossfade = " + str(e_maxcrossfade.get()) + "\n")
    preset.write("methCrsfd = " + str(c_methCrsfd.current()) + "\n")
    preset.write("crossfadechance = " + str(e_crossfadechance.get()) + "\n")
    preset.write("minFadeIn = " + str(e_minFadeIn.get()) + "\n")
    preset.write("maxFadeIn = " + str(e_maxFadeIn.get()) + "\n")
    preset.write("methFdIn = " + str(c_methFdIn.current()) + "\n")
    preset.write("fadeInChance = " + str(e_fadeInChance.get()) + "\n")
    preset.write("minFadeOut = " + str(e_minFadeOut.get()) + "\n")
    preset.write("maxFadeOut = " + str(e_maxFadeOut.get()) + "\n")
    preset.write("methFdOut = " + str(c_methFdOut.current()) + "\n")
    preset.write("fadeOutChance = " + str(e_fadeOutChance.get()) + "\n")
    preset.write("CompMethod = " + str(c_CompMethod.current()) + "\n")
    preset.write("speeds = " + str(e_speeds.get()) + "\n")
    preset.write("speedweights = " + str(e_speedweights.get()) + "\n")
    preset.write("TimeMeasure = " + str(c_TimeMeasure.current()) + "\n")
    preset.close()

def u_config_clear():
    config_empty()
    config_default()
    updatesym(0)

def check_not_filled():
    notfilled = 0
    if e_avgstrt.get()=="": notfilled = 1
    if e_strtweights.get()=="": notfilled = 1
    if e_strtdev.get()=="": notfilled = 1
    if e_normStrtChance.get()=="": notfilled = 1
    if e_stumblechance.get()=="": notfilled = 1
    if e_stumbledeviation.get()=="": notfilled = 1
    if e_minSize.get()=="": notfilled = 1
    if e_maxSize.get()=="": notfilled = 1
    if e_minPL.get()=="": notfilled = 1
    if e_maxPL.get()=="": notfilled = 1
    if e_stopChance.get()=="": notfilled = 1
    if e_reverseChance.get()=="": notfilled = 1
    if e_BackmaskCrossfade.get()=="": notfilled = 1
    if e_BackmaskChance.get()=="": notfilled = 1
    if e_reverseMaskChance.get()=="": notfilled = 1
    if e_asymmetricalBackmaskChance.get()=="": notfilled = 1
    if e_maskRepeatChance.get()=="": notfilled = 1
    if e_minMaskRepeat.get()=="": notfilled = 1
    if e_maxMaskRepeat.get()=="": notfilled = 1
    if e_repeatchance.get()=="": notfilled = 1
    if e_repeatMin.get()=="": notfilled = 1
    if e_repeatMax.get()=="": notfilled = 1
    if e_mincrossfade.get()=="": notfilled = 1
    if e_maxcrossfade.get()=="": notfilled = 1
    if e_crossfadechance.get()=="": notfilled = 1
    if e_minFadeIn.get()=="": notfilled = 1
    if e_maxFadeIn.get()=="": notfilled = 1
    if e_fadeInChance.get()=="": notfilled = 1
    if e_minFadeOut.get()=="": notfilled = 1
    if e_maxFadeOut.get()=="": notfilled = 1
    if e_fadeOutChance.get()=="": notfilled = 1
    if e_speeds.get()=="": notfilled = 1
    if e_speedweights.get()=="": notfilled = 1
    if notfilled==1: mb.showerror("Error", "Please make sure that ALL the input fields are filled!")
    return notfilled

def check_wrong_random():
    wrongrandom = 0
    if c_methDur.current()==0 and float(e_minSize.get())>float(e_maxSize.get()): wrongrandom = 1
    if c_methPause.current()==0 and float(e_minPL.get())>float(e_maxPL.get()): wrongrandom = 1
    if c_methrepmsk.current()==0 and int(float(e_minMaskRepeat.get()))>int(float(e_maxMaskRepeat.get())): wrongrandom = 1
    if c_methrep.current()==0 and int(float(e_repeatMin.get()))>int(float(e_repeatMax.get())): wrongrandom = 1
    if c_methCrsfd.current()==0 and float(e_mincrossfade.get())>float(e_maxcrossfade.get()): wrongrandom = 1
    if c_methFdIn.current()==0 and float(e_minFadeIn.get())>float(e_maxFadeIn.get()): wrongrandom = 1
    if c_methFdOut.current()==0 and float(e_minFadeOut.get())>float(e_maxFadeOut.get()): wrongrandom = 1
    if wrongrandom==1: mb.showerror("Error", "In UNIFORM random mode, the first value should be less that the second!")
    return wrongrandom

def check_imported_file():
    global importstate
    if importstate=="none":
        mb.showerror("Error", "You have to first load an audio file!")
        return 1
    elif importstate=="wait":
        mb.showerror("Import", "Please wait while importing!")
        return 1
    elif importstate=="good":
        return 0

def check_wrong_speeds():
    a = len(list(map(float, e_speeds.get().split(' '))))
    b = len(list(map(int, e_speedweights.get().split(' '))))
    if a!=b: mb.showerror("Error", "The number of speeds and their weights must match!")
    return a!=b

def check_wrong_starts():
    a = len(list(map(float, e_avgstrt.get().split(' '))))
    b = len(list(map(int, e_strtweights.get().split(' '))))
    if a!=b: mb.showerror("Error", "The number of average start times and their weights must match!")
    return a!=b

def check_zero_segment():
    a = float(e_minSize.get())
    b = float(e_maxSize.get())
    if a==0 and b==0: mb.showerror("Error", "Segment length can't be zero!")
    return a==0 and b==0

def check_wrong_lognorm():
    wrong_lognorm = 0
    if c_methDur.current()==2:
        if float(e_minSize.get())>10: wrong_lognorm = 1
        if float(e_maxSize.get())>10: wrong_lognorm = 1
    if c_methPause.current()==2:
        if float(e_minPL.get())>10: wrong_lognorm = 1
        if float(e_maxPL.get())>10: wrong_lognorm = 1
    if c_methFdIn.current()==2:
        if float(e_minFadeIn.get())>10: wrong_lognorm = 1
        if float(e_maxFadeIn.get())>10: wrong_lognorm = 1
    if c_methFdOut.current()==2:
        if float(e_minFadeOut.get())>10: wrong_lognorm = 1
        if float(e_maxFadeOut.get())>10: wrong_lognorm = 1
    if c_methCrsfd.current()==2:
        if float(e_mincrossfade.get())>10: wrong_lognorm = 1
        if float(e_maxcrossfade.get())>10: wrong_lognorm = 1
    if wrong_lognorm==1:
        wrong_lognorm = not mb.askyesno("Warning", "In LOGNORMAL random mode, parameters greater than 10 are not recommended! Continue anyway?", icon="warning")
    return wrong_lognorm

def check_config():
    return check_not_filled() or check_wrong_random() or check_imported_file() or check_wrong_speeds() or check_wrong_starts() or check_zero_segment() or check_wrong_lognorm()

def gen_import_p1(mode):
    import_thread1 = threading.Thread(target=gen_import_p2, args=(mode,))
    import_thread1.start()

def gen_import_p2(mode):
    global pathsrcaud
    global selfile
    global importstate
    global importstate_old
    importstate_old = importstate
    importstate="none"
    import_thread2 = threading.Thread(target=gen_import_p3, args=(mode,))
    import_thread2.start()
    import_thread2.join()
    if importstate=="wait":
        importstate = "none"
        mb.showerror("Import", "Wrong file format!")
    if importstate=="good" and selfile!="": mb.showinfo("Import", "Audio imported successfully.")

def gen_import_p3(mode):
    global selfile
    global importstate
    global pathsrcaud
    global audio
    if mode!="refr":
        selfile = fd.askopenfilename(filetypes=import_types, defaultextension=import_types, initialdir=defaultpaths("get", "pathsrcaud_default"))
    else:
        selfile = pathsrcaud
    if selfile=="":
        importstate = importstate_old
    else:
        pathsrcaud = selfile
        defaultpaths("set", "pathsrcaud_default")
        importstate = "wait"
        audio = AudioSegment.from_file(pathsrcaud)
        importstate = "good"

def gen_export_p1():
    if not check_config():
        global segTime
        global pathresaud
        global formatresaud
        segTime = askinteger("Export", "Exported audio length (in seconds):", initialvalue=120)
        if segTime!=None:
            pathresaud = fd.asksaveasfilename(filetypes=export_types, defaultextension=export_types, initialfile="untitled", initialdir=defaultpaths("get", "pathresaud_default"))
            if pathresaud!="":
                defaultpaths("set", "pathresaud_default")
                formatresaud = getformat(pathresaud)
                config_apply()
                export_thread = threading.Thread(target=gen_export_p2)
                export_thread.start()

def gen_export_p2():
    export_generating = threading.Thread(target=gen_main)
    export_generating.start()
    export_generating.join()
    progress['value']=0
    if gen_good==1:
        slicecr.export(pathresaud, format=formatresaud)
        OpenFile = mb.askyesno("Complete!", "Scrambling complete.\nDo you want to open your file now?", icon="info")
        if OpenFile: os.system("\"" + pathresaud + "\"")
    else:
        mb.showerror("Error", "An unknown error occurred while scrambling.")

def gen_preview_p1():
    if not check_config():
        global segTime
        segTime = sstp.get()
        config_apply()
        preview_thread = threading.Thread(target=gen_preview_p2)
        preview_thread.start()

def gen_preview_p2():
    preview_generating = threading.Thread(target=gen_main)
    preview_generating.start()
    preview_generating.join()
    progress['value']=0
    if gen_good==1:
        preview_audio = slicecr.set_sample_width(2)[0:(sstp.get()*1000)]
        play(preview_audio)
    else:
        mb.showerror("Error", "An unknown error occurred while scrambling.")

#Window
window = Tk()
window.title("AudioButcher v2.1.0-p")
window.geometry("710x370")
window.resizable(width=False, height=False)
seticon()

#Tabs
tabs = ttk.Notebook(window)
tab1 = ttk.Frame(tabs, padding=10)
tab2 = ttk.Frame(tabs, padding=10)
tabs.add(tab1, text="Main")
tabs.add(tab2, text="Advanced settings")

# Main tab
tab1_sep1 = Label(tab1)
tab1_sep2 = Label(tab1)

l_Size = Label(tab1, text="Segment length: ")
e_minSize = Entry(tab1, width=5)
s_Size = Label(tab1, text="-", width=1)
e_maxSize = Entry(tab1, width=5)
s_methDur = Label(tab1, text="/")
c_methDur = Combobox(tab1, values=randmodes, state='readonly', width=11)
c_methDur.current(0)
l_reverseChance = Label(tab1, text="Reverse chance: ")
e_reverseChance = Entry(tab1, width=3)
p_reverseChance = Label(tab1, text="%")

l_PL = Label(tab1, text="Gap length: ")
e_minPL = Entry(tab1, width=5)
s_PL = Label(tab1, text="-", width=1)
e_maxPL = Entry(tab1, width=5)
s_methPause = Label(tab1, text="/")
c_methPause = Combobox(tab1, values=randmodes, state="readonly",  width=11)
c_methPause.current(0)
l_stopChance = Label(tab1, text="Chance to stop: ")
e_stopChance = Entry(tab1, width=3)
p_stopChance = Label(tab1, text="%")
x_conspause = IntVar()
x_conspause.set(0)
c_conspause = Checkbutton(tab1, text="Allow consecutive pausing", var=x_conspause)

l_FadeIn = Label(tab1, text="Fade-in length: ")
e_minFadeIn = Entry(tab1, width=5)
s_FadeIn = Label(tab1, text="-", width=1)
e_maxFadeIn = Entry(tab1, width=5)
s_methFdIn = Label(tab1, text="/")
c_methFdIn = Combobox(tab1, values=randmodes, state="readonly", width=11)
c_methFdIn.current(0)
l_fadeInChance = Label(tab1, text="Chance to fade-in: ")
e_fadeInChance = Entry(tab1, width=3)
p_fadeInChance = Label(tab1, text="%")

l_FadeOut = Label(tab1, text="Fade-out length: ")
e_minFadeOut = Entry(tab1, width=5)
s_FadeOut = Label(tab1, text="-", width=1)
e_maxFadeOut = Entry(tab1, width=5)
s_methFdOut = Label(tab1, text="/")
c_methFdOut = Combobox(tab1, values=randmodes, state="readonly", width=11)
c_methFdOut.current(0)
l_fadeOutChance = Label(tab1, text="Chance to fade-out: ")
e_fadeOutChance = Entry(tab1, width=3)
p_fadeOutChance = Label(tab1, text="%")

l_crossfade = Label(tab1, text="Crossfade length: ")
e_mincrossfade = Entry(tab1, width=5)
s_crossfade = Label(tab1, text="-", width=1)
e_maxcrossfade = Entry(tab1, width=5)
s_methCrsfd = Label(tab1, text="/")
c_methCrsfd = Combobox(tab1, values=randmodes, state="readonly", width=11)
c_methCrsfd.current(0)
l_crossfadechance = Label(tab1, text="Chance to crossfade: ")
e_crossfadechance = Entry(tab1, width=3)
p_crossfadechance = Label(tab1, text="%")

l_repeat = Label(tab1, text="Repeat segment ... times: ")
e_repeatMin = Entry(tab1, width=5)
s_repeat = Label(tab1, text="-", width=1)
e_repeatMax = Entry(tab1, width=5)
s_methrep = Label(tab1, text="/")
c_methrep = Combobox(tab1, values=randmodes_rep, state="readonly", width=11)
c_methrep.current(0)
l_repeatchance = Label(tab1, text="Chance to repeat: ")
e_repeatchance = Entry(tab1, width=3)
p_repeatchance = Label(tab1, text="%")
x_consrep = IntVar()
x_consrep.set(0)
c_consrep = Checkbutton(tab1, text="Allow consecutive repeating", var=x_consrep)

l_avgstrt = Label(tab1, text="Average start times: ")
e_avgstrt = Entry(tab1, width=30)
l_strtdev = Label(tab1, text="Normal start deviation: ")
e_strtdev = Entry(tab1, width=6)

l_strtweights = Label(tab1, text="Start time weights: ")
e_strtweights = Entry(tab1, width=30)
l_normStrtChance = Label(tab1, text="Normal start chance: ")
e_normStrtChance = Entry(tab1, width=3)
p_normStrtChance = Label(tab1, text="%")

l_speeds = Label(tab1, text="Speed variations: ")
e_speeds = Entry(tab1, width=60)
l_speedweights = Label(tab1, text="Variation weights: ")
e_speedweights = Entry(tab1, width=60)

tab1_sep3 = Label(tab1)
l_TimeMeasure = Label(tab1, text="Time measure: ")
c_TimeMeasure = Combobox(tab1, values=timemodes, state="readonly", width=57)
l_CompMethod = Label(tab1, text="Compensation method: ")
c_CompMethod = Combobox(tab1, values=compmodes, state="readonly", width=57)

# Main tab (grid)
tab1_sep1.grid(row=0, column=6)
tab1_sep2.grid(row=0, column=10)

l_Size.grid(row=0, column=0, sticky='w')
e_minSize.grid(row=0, column=1)
s_Size.grid(row=0, column=2)
e_maxSize.grid(row=0, column=3)
s_methDur.grid(row=0, column=4)
c_methDur.grid(row=0, column=5)
l_reverseChance.grid(row=0, column=7, sticky='w')
e_reverseChance.grid(row=0, column=8)
p_reverseChance.grid(row=0, column=9)

l_PL.grid(row=1, column=0, sticky='w')
e_minPL.grid(row=1, column=1)
s_PL.grid(row=1, column=2)
e_maxPL.grid(row=1, column=3)
s_methPause.grid(row=1, column=4)
c_methPause.grid(row=1, column=5)
l_stopChance.grid(row=1, column=7, sticky='w')
e_stopChance.grid(row=1, column=8)
p_stopChance.grid(row=1, column=9)
c_conspause.grid(row=1, column=11)

l_FadeIn.grid(row=2, column=0, sticky='w')
e_minFadeIn.grid(row=2, column=1)
s_FadeIn.grid(row=2, column=2)
e_maxFadeIn.grid(row=2, column=3)
s_methFdIn.grid(row=2, column=4)
c_methFdIn.grid(row=2, column=5)
l_fadeInChance.grid(row=2, column=7, sticky='w')
e_fadeInChance.grid(row=2, column=8)
p_fadeInChance.grid(row=2, column=9)

l_FadeOut.grid(row=3, column=0, sticky='w')
e_minFadeOut.grid(row=3, column=1)
s_FadeOut.grid(row=3, column=2)
e_maxFadeOut.grid(row=3, column=3)
s_methFdOut.grid(row=3, column=4)
c_methFdOut.grid(row=3, column=5)
l_fadeOutChance.grid(row=3, column=7, sticky='w')
e_fadeOutChance.grid(row=3, column=8)
p_fadeOutChance.grid(row=3, column=9)

l_crossfade.grid(row=4, column=0, sticky='w')
e_mincrossfade.grid(row=4, column=1)
s_crossfade.grid(row=4, column=2)
e_maxcrossfade.grid(row=4, column=3)
s_methCrsfd.grid(row=4, column=4)
c_methCrsfd.grid(row=4, column=5)
l_crossfadechance.grid(row=4, column=7, sticky='w')
e_crossfadechance.grid(row=4, column=8)
p_crossfadechance.grid(row=4, column=9)

l_repeat.grid(row=5, column=0, sticky='w')
e_repeatMin.grid(row=5, column=1)
s_repeat.grid(row=5, column=2)
e_repeatMax.grid(row=5, column=3)
s_methrep.grid(row=5, column=4)
c_methrep.grid(row=5, column=5)
l_repeatchance.grid(row=5, column=7, sticky='w')
e_repeatchance.grid(row=5, column=8)
p_repeatchance.grid(row=5, column=9)
c_consrep.grid(row=5, column=11)

l_avgstrt.grid(row=6, column=0, sticky='w')
e_avgstrt.grid(row=6, column=1, columnspan=5)
l_strtdev.grid(row=6, column=7, sticky='w')
e_strtdev.grid(row=6, column=8, columnspan=2)

l_strtweights.grid(row=7, column=0, sticky='w')
e_strtweights.grid(row=7, column=1, columnspan=5)
l_normStrtChance.grid(row=7, column=7, sticky='w')
e_normStrtChance.grid(row=7, column=8)
p_normStrtChance.grid(row=7, column=9)

l_speeds.grid(row=8, column=0, sticky='w')
e_speeds.grid(row=8, column=1, columnspan=9)
l_speedweights.grid(row=9, column=0, sticky='w')
e_speedweights.grid(row=9, column=1, columnspan=9)

tab1_sep3.grid(row=10, column=0)

l_TimeMeasure.grid(row=11, column=0, sticky='w')
c_TimeMeasure.grid(row=11, column=1, columnspan=9)
c_TimeMeasure.current(0)

l_CompMethod.grid(row=12, column=0, sticky='w')
c_CompMethod.grid(row=12, column=1, columnspan=9)
c_CompMethod.current(0)

#Advanced tab
l_BackmaskCrossfade = Label(tab2, text="Backmask crossfade: ")
e_BackmaskCrossfade = Entry(tab2, width=7)
l_BackmaskChance = Label(tab2, text="Backmask chance: ")
e_BackmaskChance = Entry(tab2, width=7)
p_BackmaskChance = Label(tab2, text="%")
l_asymmetricalBackmaskChance = Label(tab2, text="Asymmetrical backmask chance: ")
e_asymmetricalBackmaskChance = Entry(tab2, width=7)
p_asymmetricalBackmaskChance = Label(tab2, text="%")
l_reverseMaskChance = Label(tab2, text="Reverse mask chance: ")
e_reverseMaskChance = Entry(tab2, width=7)
p_reverseMaskChance = Label(tab2, text="%")
l_MaskRepeat = Label(tab2, text="Repeats: ")
e_minMaskRepeat = Entry(tab2, width=2)
s_MaskRepeat = Label(tab2, text="-", width=1)
e_maxMaskRepeat = Entry(tab2, width=2)
s_methrepmsk = Label(tab2, text="/")
c_methrepmsk = Combobox(tab2, values=randmodes_rep, state="readonly", width=11)
c_methrepmsk.current(0)
l_maskRepeatChance = Label(tab2, text="Repeat chance: ")
e_maskRepeatChance = Entry(tab2, width=7)
p_maskRepeatChance = Label(tab2, text="%")
x_doublesize = IntVar()
x_doublesize.set(0)
c_doublesize = Checkbutton(tab2, text="Double size", var=x_doublesize)

tab2_sep = Label(tab2)

l_stumblechance = Label(tab2, text="Stumble chance: ")
e_stumblechance = Entry(tab2, width=13)
p_stumblechance = Label(tab2, text="%")
l_stumbledeviation = Label(tab2, text="Stumble deviation: ")
e_stumbledeviation = Entry(tab2, width=16)
l_methStumble = Label(tab2, text="Stumbling method: ")
c_methStumble = Combobox(tab2, values=stumbmodes, state="readonly", width=13)
c_methStumble.current(0)

#Advanced tab (grid)
l_BackmaskCrossfade.grid(row=0, column=0, sticky='w')
e_BackmaskCrossfade.grid(row=0, column=1, columnspan=3)
l_BackmaskChance.grid(row=1, column=0, sticky='w')
e_BackmaskChance.grid(row=1, column=1, columnspan=3)
p_BackmaskChance.grid(row=1, column=4)
l_asymmetricalBackmaskChance.grid(row=2, column=0, sticky='w')
e_asymmetricalBackmaskChance.grid(row=2, column=1, columnspan=3)
p_asymmetricalBackmaskChance.grid(row=2, column=4)
l_reverseMaskChance.grid(row=4, column=0, sticky='w')
e_reverseMaskChance.grid(row=4, column=1, columnspan=3)
p_reverseMaskChance.grid(row=4, column=4)
l_MaskRepeat.grid(row=5, column=0, sticky='w')
e_minMaskRepeat.grid(row=5, column=1)
s_MaskRepeat.grid(row=5, column=2)
e_maxMaskRepeat.grid(row=5, column=3)
s_methrepmsk.grid(row=5, column=4)
c_methrepmsk.grid(row=5, column=5)
l_maskRepeatChance.grid(row=6, column=0, sticky='w')
e_maskRepeatChance.grid(row=6, column=1, columnspan=3)
p_maskRepeatChance.grid(row=6, column=4)
c_doublesize.grid(row=7, column=0, sticky='w')

tab2_sep.grid(row=0, column=6)

l_stumblechance.grid(row=0, column=7, sticky='w')
e_stumblechance.grid(row=0, column=8)
p_stumblechance.grid(row=0, column=9)
l_stumbledeviation.grid(row=1, column=7, sticky='w')
e_stumbledeviation.grid(row=1, column=8, columnspan=2)
l_methStumble.grid(row=2, column=7, sticky='w')
c_methStumble.grid(row=2, column=8, columnspan=2)

#Menus
menu = Menu(window)
menu_file = Menu(menu, tearoff=False)
menu_help = Menu(menu, tearoff=False)
menu_sstp = Menu(menu_file, tearoff=False)
menu_file.add_command(label="Load audio file...", command=lambda: gen_import_p1("load"))
menu_file.add_command(label="Export audio...", command=lambda: gen_export_p1())
menu_file.add_command(label="Preview", command=lambda: gen_preview_p1())
menu_file.add_separator()
menu_file.add_command(label="Refresh file", command=lambda: gen_import_p1("refr"))
menu_file.add_cascade(label="Preview length", menu=menu_sstp)
sstp = IntVar()
menu_sstp.add_radiobutton(label="5 seconds", var=sstp, value=5)
menu_sstp.add_radiobutton(label="10 seconds", var=sstp, value=10)
menu_sstp.add_radiobutton(label="15 seconds", var=sstp, value=15)
menu_sstp.add_radiobutton(label="20 seconds", var=sstp, value=20)
menu_sstp.add_radiobutton(label="25 seconds", var=sstp, value=25)
menu_sstp.add_radiobutton(label="30 seconds", var=sstp, value=30)
sstp.set(10)
menu_file.add_separator()
menu_file.add_command(label="Load preset...", command=lambda: config_import())
menu_file.add_command(label="Save preset...", command=lambda: config_export())
menu_file.add_command(label="Clear all settings", command=lambda: u_config_clear())
menu_file.add_separator()
menu_file.add_command(label="Quit", command=lambda: window.destroy())
#menu_help.add_command(label="Documentation", command=lambda: mb.showinfo("Documentation", "Coming soon!"))
menu_help.add_command(label="Join our Discord server", command=lambda: webbrowser.open("https://discord.gg/gNHxMmfTy4"))
menu_help.add_separator()
menu_help.add_command(label="License...", command=lambda: license_window())
menu_help.add_command(label="About...", command=lambda: mb.showinfo("About", "AudioButcher ver. 2.1.0 (public release), June 2022 \n \nBrought to you by the AudioButcher Team: \nMightInvisible, osdwa, Shriki, vanpassinby, Zach Man"))
menu.add_cascade(label='File', menu=menu_file)
menu.add_cascade(label='Help', menu=menu_help)

#Progress bar
progress = ttk.Progressbar(window, orient="horizontal", mode="determinate", length=780)
progress.pack(side="bottom")

#User
defaultpaths("set", "all")
c_methDur.bind("<<ComboboxSelected>>", updatesym)
c_methPause.bind("<<ComboboxSelected>>", updatesym)
c_methFdIn.bind("<<ComboboxSelected>>", updatesym)
c_methFdOut.bind("<<ComboboxSelected>>", updatesym)
c_methCrsfd.bind("<<ComboboxSelected>>", updatesym)
c_methrep.bind("<<ComboboxSelected>>", updatesym)
c_methrepmsk.bind("<<ComboboxSelected>>", updatesym)
u_config_clear()
window.config(menu=menu)
tabs.pack(expand=1, fill='both', side="top")
window.mainloop()
