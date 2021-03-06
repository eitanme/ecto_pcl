#!/usr/bin/env python

"""
A VoxelGrid can be used to downsample very dense clouds.
This can be especially useful when estimating normals. 
"""

import ecto, ecto_pcl, ecto_pcl_ros
import ecto_ros, ecto_sensor_msgs
import sys

PointCloudSub = ecto_sensor_msgs.Subscriber_PointCloud2
PointCloudPub = ecto_sensor_msgs.Publisher_PointCloud2

def do_ecto():
    plasm = ecto.Plasm()

    sub = PointCloudSub("Subscriber", topic_name='/camera/rgb/points')
    
    grabber = ecto_pcl_ros.Message2PointCloud("Message2Cloud", format=ecto_pcl.XYZRGB)

    voxgrid = ecto_pcl.VoxelGrid("VGrid", leaf_size=0.05)

    pcl2msg = ecto_pcl_ros.PointCloud2Message("Cloud2Message")

    pub = PointCloudPub("Cloud Publisher", topic_name='/ecto_pcl/voxel_grid')    

    plasm.connect(sub['output'] >> grabber[:],
                  grabber[:] >> voxgrid[:],
                  voxgrid[:] >> pcl2msg[:],
                  pcl2msg[:] >> pub[:])

    sched = ecto.schedulers.Threadpool(plasm)
    sched.execute()

if __name__ == "__main__":
    ecto_ros.init(sys.argv, "voxel_grid")
    do_ecto()

