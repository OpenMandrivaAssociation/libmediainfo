%define oname	mediainfo

%define major	0
%define libname	%mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

Name:		libmediainfo
Version:	0.7.58
Release:	1
Summary:	Supplies technical and tag information about a video or audio file
Group:		System/Libraries
License:	LGLPv3+
URL:		http://mediainfo.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{oname}/%{name}_%{version}.tar.bz2
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(libzen)
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	doxygen

%description
MediaInfo supplies technical and tag information about a video or
audio file.

%package -n %{libname}
Summary:	Supplies technical and tag information about a video or audio file
Group:		System/Libraries

%description -n %{libname}
MediaInfo supplies technical and tag information about a video or
audio file.

What information can I get from MediaInfo?
* General: title, author, director, album, track number, date, duration...
* Video: codec, aspect, fps, bitrate...
* Audio: codec, sample rate, channels, language, bitrate...
* Text: language of subtitle
* Chapters: number of chapters, list of chapters

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1,
MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime,
RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3,
VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

What format (container) does MediaInfo support?
* Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...)
* Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
* Subtitles: SRT, SSA, ASS, SAMI

This package contains the shared library for MediaInfo.

%package -n %{devname}
Summary:	Include files and mandatory libraries for development
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	mediainfo-devel = %{version}-%{release}

%description -n %{devname}
Include files and mandatory libraries for development.

%prep
%setup -q -n MediaInfoLib

cp Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv History_DLL.txt History.txt

#EOLs and rights
dos2unix *.txt *.html Source/Doc/*.html
chmod 644 *.txt *.html Source/Doc/*.html

%build
export LDFLAGS="${LDFLAGS} -lzen" 
pushd Project/GNU/Library
	autoreconf -vfi
	%configure2_5x \
		--enable-shared \
		--disable-static \
		--with-libcurl \
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

%files -n %{libname}
%doc History.txt License.html ReadMe.txt
%{_libdir}/libmediainfo.so.%{major}*

%files -n %{devname}
%doc Changes.txt Doc Source/Example
%{_includedir}/MediaInfo
%{_includedir}/MediaInfoDLL
%{_libdir}/libmediainfo.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Jun 01 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.7.58-1
+ Revision: 801669
- version update 0.7.54

* Fri Mar 16 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.7.54-1
+ Revision: 785239
- version update 0.7,54

* Sat Jun 18 2011 Jani Välimaa <wally@mandriva.org> 0.7.45-1
+ Revision: 685925
- new version 0.7.45

* Tue May 03 2011 Jani Välimaa <wally@mandriva.org> 0.7.44-1
+ Revision: 664455
- import libmediainfo

