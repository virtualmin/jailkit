# jailkit (RPM)

[![Build Jailkit (RPM)](https://github.com/iliaross/jailkit/actions/workflows/build.yml/badge.svg)](https://github.com/iliaross/jailkit/actions/workflows/build.yml)

This repo builds **Jailkit** RPMs for EL-based systems, using a **Rocky Linux 8** build root for both:
- **x86_64**
- **aarch64**

## What we get

Built by GitHub Actions as artifacts:

- `jailkit-<ver>-<rel>.x86_64.rpm`
- `jailkit-<ver>-<rel>.aarch64.rpm`
- `jailkit-<ver>-<rel>.src.rpm`

## Packaging notes

- Maintainer metadata: `webmin/webmin-ci-cd <developers@virtualmin.com>`
- `jk_chrootsh` is installed with file capabilities (`cap_sys_chroot=ep`) via `%caps` in the spec.

## Local build (Rocky/EL)

```bash
dnf -y install rpm-build make gcc autoconf automake \
  glibc-devel libcap-devel python3 curl tar bzip2 patch findutils

mkdir -p rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
cp -v SPECS/jailkit.spec rpmbuild/SPECS/
cp -v SOURCES/* rpmbuild/SOURCES/ 2>/dev/null || true

# download source
VER="$(rpmspec -q --qf '%{VERSION}\n' SPECS/jailkit.spec | head -n1)"
curl -fsSL -o rpmbuild/SOURCES/jailkit-${VER}.tar.bz2 \
  "https://olivier.sessink.nl/jailkit/jailkit-${VER}.tar.bz2"

rpmbuild --define "_topdir $PWD/rpmbuild" --define "dist %{nil}" -ba rpmbuild/SPECS/jailkit.spec
