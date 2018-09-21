
#ifndef GRID_RADOS_H
#define GRID_RADOS_H

// rados configuration
hid_t fapl;

#ifdef GRID_ON_RADOS

// define constants for connection to kubernetes pool as kubernetes user
// const char *grid_rados_pool = "kubernetes";
// const char *grid_rados_user = "kubernetes";

#endif // GRID_ON_RADOS

#endif // GRID_RADOS_H
