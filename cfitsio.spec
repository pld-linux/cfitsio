# TODO: gsiftp support?
Summary:	CFITSIO Interface Library
Summary(pl.UTF-8):	Biblioteka interfejsu CFITSIO
Name:		cfitsio
# add "0" to to version to avoid epoch bumps after 3.450
%define	sver	3.49
Version:	%{sver}0
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/%{name}-%{sver}.tar.gz
# Source0-md5:	171860ffed8c1a396fc497d853f285c1
Patch0:		%{name}-zlib.patch
Patch1:		%{name}-ldflags.patch
URL:		https://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
BuildRequires:	autoconf
BuildRequires:	bzip2-devel
BuildRequires:	curl-devel
BuildRequires:	gcc-g77
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CFITSIO is a library of ANSI C routines for reading and writing FITS
format data files.  A set of Fortran-callable wrapper routines are
also included for the convenience of Fortran programmers.

%description -l pl.UTF-8
CFITSIO to biblioteka funkcji w C do odczytu i zapisu plików z danymi
w formacie FITS. Zawiera także zestaw wrapperów pozwalających na
wywoływanie tych funkcji z programów w Fortranie.

%package devel
Summary:	Header files and documentation for CFITSIO
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do CFITSIO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel

%description devel
Header files and development documentation for CFITSIO.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty do CFITSIO.

%package static
Summary:	Static CFITSIO library
Summary(pl.UTF-8):	Statyczna biblioteka CFITSIO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of CFITSIO library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki CFITSIO.

%prep
%setup -q -n %{name}-%{sver}
%patch0 -p1
%patch1 -p1

# enforce headers from system zlib
%{__rm} zlib/{crc32.h,deflate.h,inffast.h,inffixed.h,inflate.h,inftrees.h,zconf.h,zlib.h,zutil.h}

%build
%{__autoconf}
%configure \
	--with-bzip2

%{__make} shared

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

%{__make} install \
	CFITSIO_LIB=$RPM_BUILD_ROOT%{_libdir} \
	CFITSIO_INCLUDE=$RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc License.txt README docs/changes.txt
%attr(755,root,root) %{_libdir}/libcfitsio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcfitsio.so.9

%files devel
%defattr(644,root,root,755)
%doc docs/{cfortran.doc,cfitsio.ps,fitsio.doc,fitsio.ps,quick.ps}
%attr(755,root,root) %{_libdir}/libcfitsio.so
%{_includedir}/drvrsmem.h
%{_includedir}/fitsio*.h
%{_includedir}/longnam.h
%{_pkgconfigdir}/cfitsio.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcfitsio.a
