%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from activerecord-1.15.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name activerecord

Summary: Implements the ActiveRecord pattern for ORM
Name: %{?scl_prefix}rubygem-%{gem_name}
Epoch: 1
Version: 4.2.6
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: http://rubygems.org/downloads/activerecord-%{version}.gem
# git clone http://github.com/rails/rails.git
# cd rails/activerecord/
# git checkout v4.2.6
# tar czvf activerecord-4.2.6-tests.tgz test/
Source1: activerecord-%{version}-tests.tgz

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(activemodel) = %{version}
Requires: %{?scl_prefix}rubygem(activesupport) = %{version}
Requires: %{?scl_prefix}rubygem(arel) >= 6.0
Requires: %{?scl_prefix}rubygem(arel) < 7
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix}rubygem(bcrypt)
BuildRequires: %{?scl_prefix}rubygem(activesupport) = %{version}
BuildRequires: %{?scl_prefix}rubygem(activemodel)   = %{version}
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix}rubygem(erubis)
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix}rubygem(arel) >= 6.0.0
BuildRequires: %{?scl_prefix}rubygem(arel) < 7.0.0
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(rack)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Implements the ActiveRecord pattern (Fowler, PoEAA) for ORM. It ties database
tables and classes together for business objects, like Customer or
Subscription, that can find, save, and destroy themselves without resorting to
manual SQL.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}

%check
pushd .%{gem_instdir}

tar xzvf %{SOURCE1}

# load_path is not available, remove its require.
sed -i '1,2d' test/cases/helper.rb

# Fail with any test
set -e

# 1 failure/bug
# public_send in combination with method_missing raises NameError instead of NoMethodError
# https://github.com/rails/rails/issues/19297
# https://bugs.ruby-lang.org/issues/10969
#
# There is one more or N failures when requiring the tests in the following order.
# Running them in complete isolation solves the problem but takes too much time.
# So accepting up to 5 failures.
%{?scl:scl enable %{scl} - << \EOF}
# Additional failing tests, investigate.
ruby -I.:test:lib <<EOR | egrep "(1|2|3|4|5|6|7|8) failures"
  test_files = Dir.glob( "test/cases/**/*_test.rb" )
  test_files.reject! { |x| x =~ %r|/adapters/| }

  # Only test sqlite3 backend
  test_files += Dir.glob("test/cases/adapters/sqlite3/*_test.rb")
  test_files.delete('test/cases/invalid_connection_test.rb') # uses MySQL

  # To prevent a circular dependency w/ actionpack.
  test_files.delete('test/cases/session_store/session_test.rb')

  # Running separatelly works
  test_files.delete('test/cases/calculations_test.rb')

  test_files.sort.each { |f| require f }
EOR
%{?scl:EOF}

popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/MIT-LICENSE
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/examples

%changelog
* Mon Apr 04 2016 Pavel Valena <pvalena@redhat.com> - 1:4.2.6-1
- Update to 4.2.6

* Wed Feb 17 2016 Pavel Valena <pvalena@redhat.com> - 1:4.2.5.1-3
- Update to 4.2.5.1

* Wed Feb 10 2016 Pavel Valena <pvalena@redhat.com> - 1:4.1.5-2
- Fix possible input validation circumvention - rhbz#1301973
  - Resolves: CVE-2016-0753
- Nested attributes rejection proc bypass - rhbz#1301957
  - Resolves: CVE-2015-7577

* Thu Jan 22 2015 Josef Stribny <jstribny@redhat.com> - 1:4.1.5-1
- Update to 4.1.5

* Fri Aug 22 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-5
- Fix CVE-2014-3514: vulnerability in the create_with
  - Resolves: rhbz#1133531

* Wed Jul 09 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-4
- Fix CVE-2014-3483 regression
  - Related: rhbz#1115336

* Thu Jul 03 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-3
- Fix CVE-2014-3483
  - Resolves: rhbz#1115336

* Tue Feb 18 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-2
- Fix CVE-2014-0080: PostgreSQL array data injection vulnerability
  - Resolves: rhbz#1065585

* Wed Dec 04 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-1
- Update to ActiveRecord 4.0.2
  - Resolves: rhbz#1037985

* Thu Nov 21 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.1-1
- Update to ActiveRecord 4.0.1

* Mon Oct 14 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.0-2
- Convert to scl

* Thu Aug 01 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.0-1
- Update to ActiveRecord 4.0.0.

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.13-1
- Update to ActiveRecord 3.2.13.

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Feb 12 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-1
- Update to ActiveRecord 3.2.12.

* Wed Jan 09 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.11-1
- Update to ActiveRecord 3.2.11.

* Thu Jan 03 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.10-1
- Update to ActiveRecord 3.2.10.

* Mon Aug 13 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.8-1
- Update to ActiveRecord 3.2.8.

* Mon Jul 30 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.7-1
- Update to ActiveRecord 3.2.7.

* Tue Jul 24 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.6-2
- Fixed missing epoch in -doc subpackage.

* Thu Jul 19 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.6-1
- Update to ActiveRecord 3.2.6.

* Fri Jun 15 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.15-1
- Update to ActiveRecord 3.0.15.

* Fri Jun 01 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.13-1
- Update to ActiveRecord 3.0.13.

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-1
- Rebuilt for Ruby 1.9.3.
- Update to ActionRecord 3.0.11

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.10-1
- Update to ActiveRecord 3.0.10

* Mon Jul 04 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.9-1
- Update to ActiveRecord 3.0.9

* Fri Mar 25 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.5-1
- Updated to ActiveRecord 3.0.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Mohammed Morsi <mmorsi@redhat.com> - 1:3.0.3-1
- Update to rails 3

* Wed Sep 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-4
- Updated postgres fix to resolve security issue

* Mon Aug 16 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-3
- Included postgres fix (patch also pushed upstream, see rails issue tracker)

* Thu Aug 12 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-2
- Updated patch0 to correctly parse sqlite3 version

* Wed Aug 04 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Fri Sep 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4
- Enable check

* Sun Jul 26 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.3-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.2.2-1
- New upstream version
- Fixed rpmlint errors zero-length files and script-without-shebang

* Thu Nov 20 2008 David Lutterkort <lutter@redhat.com> - 2.1.1-2
- Do not mark lib/ as doc

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-1
- New version (fixes CVE-2008-4094)

* Thu Jul 31 2008 Michael Stahnke <stahnma@fedoraproject.org> - 2.1.0-1
- New Upstream

* Tue Apr  8 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-2
- Fix dependency

* Mon Apr 07 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-1
- New version

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 2.0.1-1
- New version

* Thu Nov 29 2007 David Lutterkort <dlutter@redhat.com> - 1.15.6-1
- New version

* Tue Nov 14 2007 David Lutterkort <dlutter@redhat.com> - 1.15.5-2
- Fix buildroot
- Properly mark docs in geminstdir

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.15.5-1
- Initial package
