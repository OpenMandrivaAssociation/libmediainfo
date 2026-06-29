%define		oname	MediaInfo

%define		major	0
%define		libname	%mklibname %{name}
%define		oldlibname	%mklibname %{name} 0
%define		devname %mklibname %{name} -d

Summary:	Supplies technical and tag information about a video or audio file
Name:	libmediainfo
Version:		26.05
Release:		1
License:		BSD
Group:	System/Libraries
Url:		https://mediaarea.net/
Source0:	https://mediaarea.net/download/source/libmediainfo/%{version}/%{name}_%{version}.tar.bz2
Source100:	libmediainfo.rpmlintrc
BuildRequires:		autoconf
BuildRequires:		automake
BuildRequires:		dos2unix
BuildRequires:		doxygen
BuildRequires:		libtool
BuildRequires:		libtool-base
BuildRequires:		make
BuildRequires:		pkgconfig(libcurl)
BuildRequires:		pkgconfig(libmms) >= 0.6.4
BuildRequires:		pkgconfig(libzen) >= 0.4.41
BuildRequires:		pkgconfig(tinyxml2) >= 6.0.0
BuildRequires:		pkgconfig(zlib)

%description
MediaInfo supplies technical and tag information about a video or audio file.

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Supplies technical and tag information about a video or audio file
Group:		System/Libraries
Provides:	libmediainfo = %{EVRD}
%rename %{oldlibname}

%description -n %{libname}
MediaInfo supplies technical and tag information about a video or audio file.
This package contains the shared library for MediaInfo.

%files -n %{libname}
%doc History.txt License.html ReadMe.txt
%{_libdir}/%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:		Include files and mandatory libraries for development
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	mediainfo-devel = %{EVRD}

%description -n %{devname}
Include files and mandatory libraries for development.

%files -n %{devname}
%doc Changes.txt Doc Source/Example
%{_includedir}/%{oname}
%{_includedir}/MediaInfoDLL
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n MediaInfoLib

# Drop hidden git control file
rm -f Source/Example/HowToUse_Dll-rs/.gitignore

# Rename files
cp Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv History_DLL.txt History.txt

# EOLs and rights
dos2unix *.txt *.html Source/Doc/*.html
chmod 644 *.txt *.html Source/Doc/*.html

# Don't force -O2 by default
sed -i -e "s|-O2||" Project/GNU/Library/configure.ac


%build
# Slibtool won't work with libmediainfo
ln -sf %{_bindir}/libtoolize slibtoolize
export PATH=$PWD:$PATH
export LIBTOOLIZE=%{_bindir}/libtoolize
export LIBTOOL=%{_bindir}/libtool

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
	%make_build
popd

# Generate the docs
pushd Source/Doc
        doxygen -u 2> /dev/null
        doxygen Doxyfile
popd


%install
pushd Project/GNU/Library/
	%make_install
popd

# MediaInfoDLL headers
install -dm 755 %{buildroot}%{_includedir}/%{oname}
install -m 644 Source/%{oname}/*.h %{buildroot}%{_includedir}/%{oname}
install -dm 755 %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/*.h %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.cs %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.*.java %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL*.py %{buildroot}%{_includedir}/MediaInfoDLL

# Fix and install the provided .pc file
sed -i -e 's|Version: |Version: %{version}|g' Project/GNU/Library/%{name}.pc
sed -i -e '/Libs_Static.*/d' Project/GNU/Library/%{name}.pc
install -Dm 644 Project/GNU/Library/%{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# We don't want this
#rm -rf %%{buildroot}%%{_libdir}/libmediainfo.la
