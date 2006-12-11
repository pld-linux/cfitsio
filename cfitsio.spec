Summary:	CFITSIO Interface Library
Summary(pl):	Biblioteka interfejsu CFITSIO
Name:		cfitsio
Version:	3.020
%define	sver	%(echo %{version} | tr -d .)
Release:	2
License:	GPL (forced only by gzip code, basically BSD-like)
Group:		Libraries
Source0:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sver}.tar.gz
# Source0-md5:	fbc9e0db4d4b48b0a6a8de0f2036eb47
Patch0:		%{name}-link.patch
URL:		http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
BuildRequires:	gcc-g77
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CFITSIO is a library of ANSI C routines for reading and writing FITS
format data files.  A set of Fortran-callable wrapper routines are
also included for the convenience of Fortran programmers.

%description -l pl
CFITSIO to biblioteka funkcji w C do odczytu i zapisu plików z danymi
w formacie FITS. Zawiera tak¿e zestaw wrapperów pozwalaj±cych na
wywo³ywanie tych funkcji z programów w Fortranie.

%package devel
Summary:	Header files and documentation for CFITSIO
Summary(pl):	Pliki nag³ówkowe i dokumentacja do CFITSIO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and development documentation for CFITSIO.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty do CFITSIO.

%package static
Summary:	Static CFITSIO library
Summary(pl):	Statyczna biblioteka CFITSIO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of CFITSIO library.

%description static -l pl
Statyczna wersja biblioteki CFITSIO.

%prep
%setup -q -n %{name}
%patch0 -p1

sed -i -e 's/ f77 xlf / gfortran f77 xlf /' configure

%build
%configure2_13

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
%doc License.txt README changes.txt
%attr(755,root,root) %{_libdir}/libcfitsio.so

%files devel
%defattr(644,root,root,755)
%doc cfitsio.doc cfitsio.ps fitsio.doc fitsio.ps quick.ps
%{_includedir}/*.h
%{_pkgconfigdir}/cfitsio.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcfitsio.a
