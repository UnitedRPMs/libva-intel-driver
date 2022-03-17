#
# spec file for package libva-intel-driver
#
# Copyright (c) 2022 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

#global _with_gen4asm 1
# 
%undefine _debugsource_packages
%define _legacy_common_support 1

%global commit0 3ed3f6a783fdfff3fa1b567888518dcbda7eb2a3
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:		libva-intel-driver
Version:	2.4.1
Release:	10%{?dist}
Summary:	HW video decode support for Intel integrated graphics
License:	MIT and EPL
URL:		https://01.org/linuxmedia
Source0:	https://github.com/intel/intel-vaapi-driver/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:	libtool
BuildRequires:	meson
BuildRequires:	gcc-c++

#Renamed when moved to 01.org
Provides: intel-vaapi-driver = %{version}-%{release}

%{?_with_gen4asm:BuildRequires: pkgconfig(intel-gen4asm)}
BuildRequires:	pkgconfig(libudev)
BuildRequires:	libXext-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libpciaccess-devel
BuildRequires:  libva-devel >= %{version}
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libEGL-devel
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-scanner) >= 1



%description
HW video decode support for Intel integrated graphics.


%prep
%autosetup -n intel-vaapi-driver-%{commit0} -p1

  # Only relevant if intel-gpu-tools is installed,
  # since then the shaders will be recompiled
  sed -i '1s/python$/&2/' src/shaders/gpp.py

%{?_with_gen4asm:
#Move pre-built (binary) asm code
for f in src/shaders/vme/*.g?b ; do
  mv ${f} ${f}.prebuilt
done
for f in src/shaders/h264/mc/*.g?b* ; do
  mv ${f} ${f}.prebuilt
done
}


%build

autoreconf -vif

CFLAGS+=' -fcommon'
%meson -Denable_hybrid_codec=true \
       -Dwith_x11=yes \
       -Dwith_wayland=yes \
       -Denable_tests=false \
       %{nil}

%meson_build 

%install
%meson_install

find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%{?_with_gen4asm:
#Display a diff between prebuit ASM and our generation
gendiff . .prebuilt
}


%files
%ifarch x86_64
%doc AUTHORS NEWS README
%license COPYING
%endif
%{_libdir}/dri/i965_drv_video.so


%changelog

* Mon Mar 07 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.4.1-10
- Updated to current commit

* Mon Oct 04 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.4.1-9
- Updated to current commit

* Tue Oct 27 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.4.1-8
- Updated to current commit

* Tue Jun 02 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.4.1-7
- Updated to 2.4.1

* Fri Jan 24 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.4.0-8
- Rebuilt
- Changed to meson

* Tue Nov 26 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.4.0-7
- Updated to 2.4.0-7

* Sun Sep 01 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.3.0-7
- Rebuilt

* Wed Feb 13 2019 Pavlo Rudyi <unitedrpms AT protonmail DOT com> - 2.3.0-1
- Updated to 2.3.0
- Patch for vaapi fix

* Fri Oct 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.2.0-7
- Rebuilt for libva 

* Fri Jul 13 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.2.0-1
- Updated to 2.2.0

* Mon Feb 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.1.0-1
- Updated to 2.1.0

* Sun Oct 22 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 2.0.0-1
- Updated to 2.0.0

* Thu Aug 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.8.3-2
- Enabled hybrid codec

* Wed Jul 12 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.8.3-1
- Updated to 1.8.3-1

* Thu May 25 2017 David Vásquez <davidva AT tutanota DOT com> - 1.8.2-1
- Updated to 1.8.2-1

* Thu Apr 27 2017 Pavlo Rudyi <paulcarroty at riseup.net > - 1.8.1-1
- new source URL
- updated to 1.8.1 (for F26 and F27)

* Thu Apr 27 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.7.3-2
- Rebuilt

* Wed Dec 28 2016 Pavlo Rudyi <paulcarroty at riseup.net > - 1.7.3-1
- Updated to 1.7.3

* Tue Sep 06 2016 Pavlo Rudyi <paulcarroty at riseup.net > - 1.7.2-1
- Updated to 1.7.2

* Fri Jul 08 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.7.1-2
- Massive rebuild

* Sun Jul 03 2016 Pavlo Rudyi <paulcarroty at riseup.net > - 1.7.1-1
- Updated to 1.7.1

* Wed Apr 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.7.0-1
- Updated to 1.7.0

* Thu Dec 17 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.1-1
- Update to 1.6.1

* Tue May 05 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Tue Oct 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 02 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Sat Apr 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-2
- Add missing wayland-scanner BR

* Sat Apr 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Tue Mar 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-2
- Backport patch - rhbz#3193

* Mon Feb 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Tue Oct 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Wed Jun 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Wed Mar 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.20-1
- Update to 1.0.20
- Spec file clean-up

* Fri Nov 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.19-1
- Update to 1.0.19

* Fri Aug 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-4
- Update to final 1.0.18

* Wed Jul 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-3
- Switch to pkgconfig(libudev)

* Mon Jun 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-1
- Update to 1.0.18

* Sat May 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-4
- Introduce --with gen4asm

* Tue Jan 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-3
- Add BR intel-gen4asm
- Move pre-built asm code
- Adjust license with EPL

* Mon Jan 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-2
- Spec cleanup

* Thu Nov 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-1
- Rename the package to libva-intel-driver

* Sun Aug 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.14-1
- Update to 1.0.14

* Sat Jun 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-2
- Fix typo when building --with full
- Requires at least the same libva version.

* Wed Jun 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-1
- Update to 1.0.13

* Sun Apr 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.12-1
- Update to 1.0.12

* Thu Mar 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Switch to additional package using the freedesktop version
- Add git rev from today as patch

* Mon Feb 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Tue Jan 25 2011 Adam Williamson <awilliam@redhat.com> - 1.0.8-1
- bump to new version
- fix modded tarball to actually not have i965 dir
- merge with the other spec I seem to have lying around somewhere

* Wed Nov 24 2010 Adam Williamson <awilliam@redhat.com> - 1.0.6-1
- switch to upstream from sds branch (sds now isn't carrying any very
  interesting changes according to gwenole)
- pull in the dont-install-test-programs patch from sds
- split out libva-utils again for multilib purposes
- drop -devel package obsolete/provides itself too

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-3.sds4
- drop obsoletes and provides of itself (hangover from freeworld)

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-2.sds4
- fix the tarball to actually remove the i965 code (duh)

* Thu Oct 7 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-1.sds4
- initial package (based on package from elsewhere by myself and Nic
  Chauvet with i965 driver removed)
