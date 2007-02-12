Summary:	Wake-On-Lan support for nVidia nForce ethernet drivers
Summary(pl.UTF-8):	Wsparcie dla Wake-On-Lan dla kart sieciowych nVidia nForce
Name:		forcedeth-wol
Version:	1.1
Release:	1
License:	GPL
Group:		Networking
Source0:	ftp://ep09.pld-linux.org/people/siefca/software/%{name}-%{version}.tar.gz
# Source0-md5:	cae4cce72d9316a37106b03d9a2ba1aa
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	ethtool
Requires:	rc-scripts
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		localedir	/etc/sysconfig/locale
%define		_sbindir	/sbin

%description
nVidia nForce on-board ethernet drivers cannot correctly enter in the
sleep state. This causes problems with Wake-On-Lan feature. This
package implements work-around to fix it. For fine working the patched
forcedeth kernel driver is also required.

%description -l pl.UTF-8
Sterowniki dla kart sieciowych nVidia nForce nie potrafią tak ustawić
karty, aby mogła ona samodzielnie wejść w stan uśpienia. Sprawia to
kłopoty z obsługą funkcji Wake-On-Lan. Ten pakiet implementuje
obejście, aby ta funkcjonalność była możliwa. Do prawidłowego
działania wymagany jest dodatkowo odpowiednio spreparowany moduł jądra
forcedeth.

%prep
%setup -q

%build
%configure \
	--with-localedir=%{localedir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add forcedeth-wol
%service forcedeth-wol restart

%preun
if [ "$1" = "0" ]; then
	%service forcedeth-wol stop
	/sbin/chkconfig --del forcedeth-wol
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%doc doc/README*.txt doc/linux-*WON.patch
%attr(754,root,root) /etc/rc.d/init.d/forcedeth-wol
%attr(755,root,root) %{_sbindir}/pci-config

%lang(pl) %{localedir}/pl/LC_MESSAGES/forcedeth-wol.mo
