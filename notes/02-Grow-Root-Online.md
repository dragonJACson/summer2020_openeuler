---
title: Grow Root Online
date: 2020-07-11 14:44:34
---

## 提出问题

使用 `dd` 将树莓派镜像写入 16 GiB 的内存卡后，系统中 `root` 分区的可用空间只有 1.6 GiB，很明显，这并不够用，也浪费了内存卡里剩余的空间，那么我们如何在不 `umount` `root` 分区，也不借助其他电脑的情况下，对 `root` 分区进行扩容呢？

## 解决问题

首先我们使用 `fdisk` 来进行重新分区，`fdisk` 在删除分区后，该分区的数据并没有立即删除，我们只需在与原本的 `root` 分区的起始位置的同一个 sector 新建分区即可。

```
# fdisk /dev/mmcblk0

Command (m for help): p
```

```
Disk /dev/mmcblk0: 14.86 GiB, 15931539456 bytes, 31116288 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk Identifier: 0xed0b82cb

Device         Boot   Start         End Sectors  Size Id Type
/dev/mmcblk0p1 *       8192      593919  585728  286M  c W95 FAT32 (LBA)
/dev/mmcblk0p2       593920     1593343  999424  488M 82 Linux swap / Solaris
/dev/mmcblk0p3      1593344     4872191 3278848  1.6G 83 Linux
```

可以看到 `root` 分区是第三个分区，大小只有 1.6 GiB，起始 sector 是 1593344，我们直接删除该分区并重新建一个

```
Command (m for help): d
Partition number (1-3, default 3): 3

Partition 3 has been deleted.

Command (m for help): n
Partition type
   p   primary (2 primary, 0 extended, 2 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (3,4, default 3): 3
First sector (2048-31116287, default 2048): 1593344
Last sector, +/-sectors or +/-size{K,M,G,T,P} (1593344-31116287, default 31116287): 31116287

Created a new partition 3 of type 'Linux' and of size 14.1 GiB.
Partition #3 contains a ext4 signature.

Do you want to remove the signature? [Y]es/[N]o: N

Command (m for help): w
```

现在就可以重启了。重启以后，我们执行 `df -h /`，可以发现

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       1.6G  1.5G  9.5M 100% /
```

似乎没有变化？其实我们还需要执行一个命令

```
# resize2fs /dev/mmcblk0p3
resize2fs 1.45.3 (14-Jul-2019)
Filesystem at /dev/mmcblk0p3 is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 2
The filesystem on /dev/mmcblk0p3 is now 3690360 (4k) blocks long.
````

再执行一次 `df -h /`，完美

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        14G  1.5G   12G  11% /
```
