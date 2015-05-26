class UnixOsAdapter:
  @staticmethod
  def dd(i, o):
    glue = '| pv | sudo dd'
    if not '/dev/' in i: #raw devices dont work
      glue = '| pv --size=$(%s) | sudo dd' % UnixOsAdapter.files_size_byte(i)

    return "sudo dd if=%s %s of=%s bs=1m" % (i, glue, o)

  @staticmethod
  def files_size_byte(path):
    return "ls -nl %s | awk '{print $5}'" % path

  @staticmethod
  def unmount(dev):
    return "sudo umount %s || echo ''" % dev

  @staticmethod
  def mk_fat_32(dev):
    return "sudo mkfs.vfat %s" % dev

  @staticmethod
  def list_devices():
    return "ls -al /dev/sd* | grep '/dev/sd[0-9]*$'"

wrapper = UnixOsAdapter
