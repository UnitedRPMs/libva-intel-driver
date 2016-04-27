#global _with_gen4asm 1

Name:		libva-intel-driver
Version:	1.6.2
Release:	1%{?dist}
Summary:	HW video decode support for Intel integrated graphics
Group:		System Environment/Libraries
License:	MIT and EPL
URL:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/%{name}/%{name}-%{version}.tar.bz2

ExclusiveArch:	%{ix86} x86_64 ia64

#BuildRequires:	libtool

%{?_with_gen4asm:BuildRequires: pkgconfig(intel-gen4asm)}
BuildRequires:	pkgconfig(libudev)
BuildRequires:	libXext-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libpciaccess-devel
BuildRequires:	libva-devel >= 1.3.0
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libEGL-devel
%{!?_without_wayland:
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-scanner) >= 1
}


%description
HW video decode support for Intel integrated graphics.


%prep
%setup -q
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
#autoreconf -vif
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%{?_with_gen4asm:
#Display a diff between prebuit ASM and our generation
gendiff . .prebuilt
}


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/dri/i965_drv_video.so


%changelog
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
