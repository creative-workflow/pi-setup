import linux

class OsxOsAdapter(linux.UnixOsAdapter):
  @staticmethod
  def unmount(dev):
    return "sudo diskutil unmountDisk %s || echo ''" % dev

  @staticmethod
  def mk_fat_32(dev):
    return "sudo newfs_msdos -F 32 %s" % dev

  @staticmethod
  def list_devices():
    return "ls -al /dev/disk* | grep '/dev/disk[0-9]*$'"

wrapper = OsxOsAdapter
