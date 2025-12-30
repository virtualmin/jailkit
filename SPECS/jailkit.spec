%global upstream_version 2.23
%global __requires_exclude_from ^/usr/(s)?bin/jk_.*

Name:           jailkit
Version:        %{upstream_version}%{?build_number}
Release:        %{?pkgrel}%{!?pkgrel:1}%{?dist}
Summary:        Tools to generate chroot jails easily
License:        BSD-3-Clause AND LGPL-2.0-or-later
URL:            https://olivier.sessink.nl/jailkit/

Packager:       webmin/webmin-ci-cd <developers@virtualmin.com>
Vendor:         Virtualmin

Source0:        https://olivier.sessink.nl/jailkit/jailkit-%{upstream_version}.tar.bz2
Patch1:         jailkit-2.17-makefile.patch
Patch2:         jailkit-jk_init-php.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  glibc-devel
BuildRequires:  libcap-devel
BuildRequires:  python3

Requires:       python3

%description
Jailkit is a set of utilities to limit user accounts to specific files using
chroot() and or specific commands. Setting up a chroot shell, a shell limited
to some specific command or a daemon inside a chroot jail is a lot easier and
can be automated using these utilities.

Jailkit is a specialized tool that is developed with a focus on security. It
will abort in a secure way if the configuration, the system setup or the
environment is not 100% secure, and it will send useful log messages that
explain what is wrong to syslog.

Jailkit is known to be used in network security appliances from several
leading IT security firms, Internet servers from several large enterprise
organizations, Internet servers from Internet service providers, as well as
many smaller companies and private users that need to secure login in services
or in daemon processes.

Currently, Jailkit provides jails for cvs, git, scp, sftp, ssh, rsync,
procmail, openvpn, vnc, etc.

Jailkit provides the following commands: jk_check, jk_chrootlaunch,
jk_chrootsh, jk_cp, jk_init, jk_jailuser, jk_list, jk_lsh, jk_socketd,
jk_uchroot, jk_update.

%prep
%setup -q -n %{name}-%{upstream_version}
%patch1 -p0 -b .makefile
%patch2 -p0

%build
%configure PYTHON=%{__python3}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

# Make sure jk_chrootsh is NOT setuid; we rely on file capabilities instead
chmod u-s %{buildroot}%{_sbindir}/jk_chrootsh || true

# Forbid ambiguous /usr/bin/python and /usr/libexec/platform-python shebangs
find %{buildroot}%{_sbindir} -maxdepth 1 -type f -name 'jk_*' -print0 | \
  xargs -0r sed -i \
    -e '1 s|^#! */usr/bin/python$|#!/usr/bin/python3|' \
    -e '1 s|^#! */usr/libexec/platform-python$|#!/usr/bin/python3|'

%{__install} -Dp -m0755 extra/jailkit %{buildroot}%{_initrddir}/jailkit

%post
if [ -w %{_sysconfdir}/shells ] && \
   ! grep -qxF "%{_sbindir}/jk_chrootsh" %{_sysconfdir}/shells
then
  echo "%{_sbindir}/jk_chrootsh" >> %{_sysconfdir}/shells
fi

%postun
if [ $1 -eq 0 ]; then
  sed -i -e "/jk_chrootsh/d" %{_sysconfdir}/shells
fi

%files
%defattr(-, root, root, 0755)
%license COPYRIGHT
%doc README.txt INSTALL.txt
%doc %{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/jailkit/
%config %{_initrddir}/jailkit
%caps(cap_sys_chroot=ep) %{_sbindir}/jk_chrootsh
%{_sbindir}/jk_jailuser
%{_sbindir}/jk_socketd
%{_sbindir}/jk_check
%{_sbindir}/jk_cp
%{_sbindir}/jk_list
%{_sbindir}/jk_update
%{_sbindir}/jk_chrootlaunch
%{_sbindir}/jk_init
%{_sbindir}/jk_lsh
%{_bindir}/jk_uchroot
%{_datadir}/jailkit/

%changelog
* Wed Dec 24 2025 Ilia Ross <ilia@virtualmin.com> - 2.23-1
- Update to version 2.23
- Add arm64 support
- Add python3 runtime dependency
- Keep jk_chrootsh capability via %caps

* Sun Aug 15 2021 Joe Cooper <joe@virtualmin.com> - 2.22-1
- Bump rev to latest version
- which fixes bogus includesections config in jk_init.ini

* Sat Jan 04 2020 Joe Cooper <joe@virtualmin.com> - 2.21-1
- Bump rev to latest version
- Remove mention of jk_addjailuser (removed upstream)

* Tue May 30 2017 Joe Cooper <joe@virtualmin.com> - 2.19-4
- Patch jk_init.ini to include a php section

* Tue Dec 06 2016 Joe Cooper <joe@virtualmin.com> - 2.19-1
- Update to 2.19
- Apply patch and changes suggested in https://bugzilla.redhat.com/show_bug.cgi?id=967782
- setcap on jk_chrootsh with %caps macro

* Wed Jun 02 2010 Steve Huff <shuff@vecna.org> - 2.11-1 - 8843/shuff
- Updated to release 2.11.

* Thu May 15 2008 Dries Verachtert <dries@ulyssis.org> - 2.5-1
- Updated to release 2.5.

* Tue Sep 12 2006 Dag Wieers <dag@wieers.com> - 2.1-1
- Updated to release 2.1.

* Sun Mar 19 2006 Dag Wieers <dag@wieers.com> - 2.0-1
- Updated to release 2.0.

* Fri May 20 2005 Dag Wieers <dag@wieers.com> - 1.3-1
- Initial package. (using DAR)
