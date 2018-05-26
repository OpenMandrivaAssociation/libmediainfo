%define oname	mediainfo

%define major	0
%define libname	%mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

Name:		libmediainfo
Version:	18.03
Release:	1
Summary:	Supplies technical and tag information about a video or audio file
Group:		System/Libraries
License:	BSD
URL:		http://mediaarea.net/
Source0:	http://mediaarea.net/download/source/libmediainfo/%{version}/libmediainfo_%{version}.tar.bz2
Patch0:		libmediainfo_0.7.70-pkgconfig.patch

BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libzen) >= 0.4.37
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libmms) >= 0.6.4
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(tinyxml2) >= 6.0.0

%description
MediaInfo supplies technical and tag information about a video or
audio file.

%package -n %{libname}
Summary:	Supplies technical and tag information about a video or audio file
Group:		System/Libraries
Provides:	libmediainfo

%description -n %{libname}
MediaInfo supplies technical and tag information about a video or
audio file.
This package contains the shared library for MediaInfo.


%files -n %{libname}
%doc History.txt License.html ReadMe.txt
%{_libdir}/libmediainfo.so.%{major}*

#----------------------------------------------------------------------------
%package -n %{devname}
Summary:	Include files and mandatory libraries for development
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	mediainfo-devel = %{EVRD}

%description -n %{devname}
Include files and mandatory libraries for development.


%files -n %{devname}
%doc Changes.txt Doc Source/Example
%{_includedir}/MediaInfo
%{_includedir}/MediaInfoDLL
%{_libdir}/libmediainfo.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------
%prep
%setup -qn MediaInfoLib
%patch0 -p1

# Rename files
cp Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv History_DLL.txt History.txt

# EOLs and rights
dos2unix *.txt *.html Source/Doc/*.html
chmod 644 *.txt *.html Source/Doc/*.html

# Don't force -O2 by default
sed -i -e "s|-O2||" Project/GNU/Library/configure.ac

%build
pushd Project/GNU/Library
	autoreconf -vfi
	export CPPFLAGS="-DMEDIAINFO_LIBMMS_DESCRIBE_SUPPORT=0"
	%configure \
		--enable-shared \
		--disable-static \
		--with-libcurl \
		--with-libmms \
		--with-libaes=no \
		--with-libmd5=no \
		--with-libtinyxml2 \
		--enable-visibility
	%make
popd

# generate docs
pushd Source/Doc
        doxygen -u 2> /dev/null
        doxygen Doxyfile
popd

%install
pushd Project/GNU/Library/
	%makeinstall_std
popd

# MediaInfoDLL headers
install -dm 755 %{buildroot}%{_includedir}/MediaInfo
install -m 644 Source/MediaInfo/*.h %{buildroot}%{_includedir}/MediaInfo
install -dm 755 %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/*.h %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.cs %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.*.java %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL*.py %{buildroot}%{_includedir}/MediaInfoDLL

#fix and instal .pc file
sed -i -e 's|Version: |Version: %{version}|g' Project/GNU/Library/libmediainfo.pc
sed -i -e '/Libs_Static.*/d' Project/GNU/Library/libmediainfo.pc

install -Dm 644 Project/GNU/Library/libmediainfo.pc %{buildroot}%{_libdir}/pkgconfig/libmediainfo.pc

#we don't want these
rm -rf %{buildroot}%{_libdir}/libmediainfo.la




