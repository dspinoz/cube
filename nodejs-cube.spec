%{?nodejs_find_provides_and_requires}

Name:           nodejs-cube
Version:        0.2.12
Release:        6%{?dist}
Summary:        Cube is a system for collecting timestamped events and deriving metrics.

Group:          Node
License:        Apache License, Version 2.0

#Upstream http://square.github.io/cube/
#URL:            https://registry.npmjs.org/cube/-/cube-0.2.12.tgz

# Fork - Github
#URL:            https://github.com/dspinoz/cube/archive/master.tgz

Source:			cube-0.2.12-6.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

Requires:       nodejs-ctype /usr/bin/mongod
BuildRequires:  nodejs-devel nodejs-vows nodejs-pegjs

%description
Cube is a system for collecting timestamped events and deriving metrics. 
By collecting events rather than metrics, Cube lets you compute aggregate 
statistics post hoc. It also enables richer analysis, such as quantiles 
and histograms of arbitrary event sets. Cube is built on MongoDB and 
available under the Apache License.

Want to learn more? See the wiki.

%package collectd
Summary:        Collectd configuration for posting events to cube
Requires:       collectd

%description collectd
Collectd configuration for posting events to cube

%prep
%setup -q -n cube.git

cat > collectd.conf <<EOF
LoadPlugin logfile
<Plugin logfile>
	LogLevel info
	File "/var/log/collectd.log"
	Timestamp true
</Plugin>

LoadPlugin write_http
<Plugin write_http>
	<URL "http://localhost:1080/collectd">
		Format "JSON"
	</URL>
</Plugin>
EOF

%build
make 

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/cube
mv bin/collector-config.js bin/evaluator-config.js %{buildroot}%{_sysconfdir}/cube

mkdir -p %{buildroot}%{nodejs_sitelib}/cube
cp -pr bin lib package.json LICENSE README.md static %{buildroot}%{nodejs_sitelib}/cube

mkdir -p %{buildroot}%{_bindir}
ln -sf %{nodejs_sitelib}/cube/bin/collector.js %{buildroot}%{_bindir}/cube-collector
ln -sf %{nodejs_sitelib}/cube/bin/evaluator.js %{buildroot}%{_bindir}/cube-evaluator

#collectd
install -D collectd.conf %{buildroot}%{_sysconfdir}/collectd.d/cube.conf


%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/cube
%config %_sysconfdir/cube/collector-config.js
%config %_sysconfdir/cube/evaluator-config.js
%{_bindir}/cube-collector
%{_bindir}/cube-evaluator

%files collectd
%config %_sysconfdir/collectd.d/cube.conf


%changelog
* Thu Nov 05 2015 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-6
- Allow any reducer values values to be saved into database, not just Double
- distinct_each returns an array containing a set of objects with key and value attributes
* Thu Oct 22 2015 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-5
- add distinct_each reducer
- better error reporting for event and metric parsers
* Thu Oct 22 2015 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-4
- New build, maintaining own fork of https://github.com/square/cube at https://github.com/dspinoz/cube
- Spec file from https://github.com/dspinoz/nodejs/nodejs-cube.spec
- Removed patches from spec file and commited into forked git repository
- Hopefully will be pushed upstream at some stage
* Tue Nov 18 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-3
- Add pull request #86 to allow event subtyping
* Tue Aug 19 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-2
- optional package for posting collectd events to cube
* Mon Aug 11 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-1
- packaged for installation on redhat using epel nodejs
