Summary:	CFITSIO Interface Library
Summary(pl):	Biblioteka interfejsu CFITSIO
Name:		cfitsio
Version:	2.420
%define	sver	%(echo %{version} | tr -d .)
Release:	1
License:	GPL (forced only by gzip code, basically BSD-like)
Group:		Libraries
Source0:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sver}.tar.gz
URL:		http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
BuildRequires:	gcc-g77
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
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for CFITSIO.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty do CFITSIO.

%package static
Summary:	Static CFITSIO library
Summary(pl):	Statyczna biblioteka CFITSIO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of CFITSIO library.

%description static -l pl
Statyczna wersja biblioteki CFITSIO.

%prep
%setup -q -n %{name}

%build
%configure2_13

%{__make} shared all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

%{__make} install \
	FTOOLS_LIB=$RPM_BUILD_ROOT%{_libdir} \
	FTOOLS_INCLUDE=$RPM_BUILD_ROOT%{_includedir}

install libcfitsio.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Licence.txt README changes.txt
%attr(755,root,root) %{_libdir}/lib*.so

%files devel
%defattr(644,root,root,755)
%doc cfitsio.doc cfitsio.ps fitsio.doc fitsio.ps quick.ps
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
