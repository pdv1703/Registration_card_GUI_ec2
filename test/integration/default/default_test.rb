require 'inspec'

describe file('/home/remote/HistoryStatistic.py') do
 it { should exist }
end

describe yum do
  its('epel') { should exist }
  its('epel') { should be_enabled }
end

describe package('yum-utils') do
  it { should be_installed }
end

describe package('epel-release') do
  it { should be_installed }
end

describe package('python36u') do
  it { should be_installed }
end

describe package('python36u-pip') do
  it { should be_installed }
end

describe command("sudo yum grouplist | sed '/^Installed Groups:/,$!d;/^Available Groups:/,$d;/^Installed Groups:/d;s/^[[:space:]]*//' | grep 'KDE Desktop'") do
  its('stdout') { should eq "KDE Desktop\n" }
  #its('stderr') { should eq '' }
  its('exit_status') { should eq 0 }
end

