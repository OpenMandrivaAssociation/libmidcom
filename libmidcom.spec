%define	major 1
%define libname	%mklibname midcom %{major}

Summary:	The MIDCOM SIMCO protocol and Timer library
Name:		libmidcom
Version:	0.1.0
Release:	%mkrel 2
Group:		System/Libraries
License:	GPL
URL:		http://www.ranchnetworks.com/
Source0:	http://ftp.digium.com/pub/telephony/asterisk/%{name}-%{version}.tar.bz2
BuildRequires:	openssl-devel
BuildRequires:	dos2unix

%description
The MIDCOM SIMCO protocol and Timer library

%package -n	%{libname}
Summary:	The MIDCOM SIMCO protocol and Timer library
Group:          System/Libraries

%description -n	%{libname}
The MIDCOM SIMCO protocol and Timer library

%package -n	%{libname}-devel
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
The MIDCOM SIMCO protocol and Timer library

This package contains the static %{name} library and its header
files.

%prep

%setup -q -n %{name}-%{version}

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%build

pushd midcom
    make \
	SSL_LIB_DIR="-L%{_libdir}" \
	SSL_INCLUDE_DIR="-I%{_includedir}/openssl" \
	SSL_LIBS="-lssl -lcrypto" \
	CFLAGS="%{optflags} -fPIC" \
	SOFLAGS="-Wl,-hlibmidcom.so.%{major} -Wl,-soname=libmidcom.so.%{major}" \
	STATIC_LIBRARY="libmidcom.a" \
	DYNAMIC_LIBRARY="libmidcom.so.%{major}.0"
popd

pushd timer
    make \
	CFLAGS="%{optflags} -fPIC" \
	SOFLAGS="-Wl,-hlibtimer.so.%{major} -Wl,-soname=libtimer.so.%{major}" \
	STATIC_LIBRARY="libtimer.a" \
	DYNAMIC_LIBRARY="libtimer.so.%{major}.0"
popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/midcom
install -d %{buildroot}%{_includedir}/timer

install -m0755 midcom/libmidcom.so.%{major}.0 %{buildroot}%{_libdir}/
ln -s libmidcom.so.%{major}.0 %{buildroot}%{_libdir}/libmidcom.so.%{major}
ln -s libmidcom.so.%{major} %{buildroot}%{_libdir}/libmidcom.so
install -m0644 midcom/libmidcom.a %{buildroot}%{_libdir}/
install -m0644 midcom/simco_client.h %{buildroot}%{_includedir}/midcom/

install -m0755 timer/libtimer.so.%{major}.0 %{buildroot}%{_libdir}/
ln -s libtimer.so.%{major}.0 %{buildroot}%{_libdir}/libtimer.so.%{major}
ln -s libtimer.so.%{major} %{buildroot}%{_libdir}/libtimer.so
install -m0644 timer/libtimer.a %{buildroot}%{_libdir}/
install -m0644 timer/*.h %{buildroot}%{_includedir}/timer/

# fix headers
pushd %{buildroot}%{_includedir}/timer
    for h in *.h; do
	perl -pi -e "s|\"$h\"|\<timer/$h\>|g" *.h
    done
popd

pushd %{buildroot}%{_includedir}/midcom
    for h in *.h; do
	perl -pi -e "s|\"$h\"|\<midcom/$h\>|g" *.h
    done
popd

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc gpl.txt
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/midcom/*
%{_includedir}/timer/*
%{_libdir}/*.so
%{_libdir}/*.a


