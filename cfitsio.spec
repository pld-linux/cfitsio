Summary:	CFITSIO Interface Library
Summary(pl.UTF-8):	Biblioteka interfejsu CFITSIO
Name:		cfitsio
Version:	3.370
%define	sver	%(echo %{version} | tr -d .)
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sver}.tar.gz
# Source0-md5:	abebd2d02ba5b0503c633581e3bfa116
Patch0:		%{name}-ldflags.patch
Patch1:		%{name}-zlib.patch
URL:		http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
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
%setup -q -n %{name}
%patch0 -p0
%patch1 -p1

# enforce headers from system zlib
%{__rm} zlib/{crc32.h,deflate.h,inffast.h,inffixed.h,inflate.h,inftrees.h,zconf.h,zlib.h,zutil.h}

%build
%configure

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
%attr(755,root,root) %ghost %{_libdir}/libcfitsio.so.2

%files devel
%defattr(644,root,root,755)
%doc docs/{cfitsio.doc,cfitsio.ps,fitsio.doc,fitsio.ps,quick.ps}
%attr(755,root,root) %{_libdir}/libcfitsio.so
%{_includedir}/drvrsmem.h
%{_includedir}/fitsio*.h
%{_includedir}/longnam.h
%{_pkgconfigdir}/cfitsio.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcfitsio.a
