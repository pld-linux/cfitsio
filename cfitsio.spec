# TODO: gsiftp support? (--with-gsiftp, --with-gsiftp-flavour=$flavour; BR: libglobus_ftp_client_${flavour}; https://github.com/gridcf/gct/ etc.)
#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	CFITSIO Interface Library
Summary(pl.UTF-8):	Biblioteka interfejsu CFITSIO
Name:		cfitsio
Version:	4.6.2
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/%{name}-%{version}.tar.gz
# Source0-md5:	38e1510bf8e19fd3b7fabebf84009287
URL:		https://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
BuildRequires:	bzip2-devel
BuildRequires:	curl-devel
BuildRequires:	gcc-g77
BuildRequires:	rpmbuild(macros) >= 1.527
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
%setup -q

%build
%configure \
	%{__enable_disable static_libs static} \
	--with-bzip2

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcfitsio.la

# too common names; if needed, use subdir for cfitsio headers
%{__rm} $RPM_BUILD_ROOT%{_includedir}/{cfortran,f77_wrap}.h

# testing tools
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{cookbook,smem,speed}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README.md licenses/License.txt
%attr(755,root,root) %{_bindir}/fitscopy
%attr(755,root,root) %{_bindir}/fitsverify
%attr(755,root,root) %{_bindir}/fpack
%attr(755,root,root) %{_bindir}/funpack
%attr(755,root,root) %{_bindir}/imcopy
%attr(755,root,root) %{_libdir}/libcfitsio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcfitsio.so.10

%files devel
%defattr(644,root,root,755)
%doc docs/{cfitsio.pdf,cfortran.doc,fitsio.pdf,fpackguide.pdf,quick.pdf}
%attr(755,root,root) %{_libdir}/libcfitsio.so
%{_includedir}/drvrsmem.h
%{_includedir}/fitsio*.h
%{_includedir}/longnam.h
%{_includedir}/region.h
%{_pkgconfigdir}/cfitsio.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcfitsio.a
%endif
