# Networking & Architecture Assessment

This folder contains the files for my Master's Networking and Architecture assessment. I have updated the configuration in alignment with the feedback received from my original submission.
The project involved configuring routing, DHCP, and firewall behaviour for a multi-router network spanning internal (Talos), DMZ, and external (Delos) segments.

---

## Included Files

- **Network_Configuration_updated.imn**
  The CORE/IMUNES simulation file containing all router, switch, host, routing, DHCP, and firewall configurations.

- **Network_Topology.png**
  A picture of the full network layout used in the assessment.

- **README.md**

---

## Assessment Summary

The assessment consisted of three main practical tasks:

### **Task A - Routing**
Configure static routes across R1, R2, R3, and R4 to ensure full connectivity and optimal path selection within the Talos and Delos networks.

### **Task B - DHCP**
Set up a DHCP server on Minerva to dynamically assign IP addresses to Delos clients while keeping the private server, leto, statically addressed.

### **Task C - Firewall**
Configure R3 as a stateful firewall controlling traffic between internal, DMZ, and external networks, allowing only the required services and dropping all other traffic.

---

## Notes

All routing, DHCP, and firewall logic is contained inside the `.imn` file.
This folder serves as a clean snapshot of the assessment setup, including the topology and simulation environment.
