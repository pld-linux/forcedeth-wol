Summary:	Wake-On-Lan support for nVidia nForce ethernet drivers
Summary(pl):	Wsparcie dla Wake-On-Lan dla kart sieciowych nVidia nForce
Name:		forcedeth-wol
Version:	1.0
Release:	1
License:	GPL
Group:		Base
Source0:	ftp://ep09.pld-linux.org/people/siefca/software/%{name}-%{version}.tar.gz
# Source0-md5:	650fa5aeb21e8fa62aa7f7b1d76c7a26
Requires:	rc-scripts
Requires:	ethtool
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		localedir	/etc/sysconfig/locale
%define		_sbindir	/sbin

%description
nVidia nForce on-board ethernet drivers cannot correctly enter
in the sleep state. This causes problems with Wake-On-Lan feature.
This package implements work-around to fix it. For fine working
the patched forcedeth kernel driver is also required.

%description -l pl
Sterowniki dla kart sieciowych nVidia nForce nie potrafi± tak ustawiæ
karty, aby mog³a ona samodzielnie wej¶æ w stan u¶pienia. Sprawia to
k³opoty z obs³ug± funkcji Wake-On-Lan. Ten pakiet implementuje obej¶cie,
aby ta funkcjonalno¶æ by³a mo¿liwa. Do prawid³owego dzia³ania wymagany
jest dodatkowo odpowiednio spreparowany modu³ kernela forcedeth.

%prep
%setup -q

%build
%configure \
	--with-localedir=%{localedir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install DESTDIR=$RPM_BUILD_ROOT
	
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add forcedeth-wol

%postun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del forcedeth-wol
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%doc doc/*.txt doc/linux-*WON.patch

%attr(754,root,root) /etc/rc.d/init.d/forcedeth-wol
%attr(755,root,root) %{_sbindir}/pci-config

%dir %{localedir}
%lang(pl) %{localedir}/pl
