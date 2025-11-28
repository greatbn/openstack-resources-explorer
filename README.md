# os-explorer

A CLI + Terminal UI tool to discover OpenStack resources, build a relationship graph, and visualize it.

## Installation

```bash
pip install .
```

## Configuration

`os-explorer` uses `openstacksdk` for authentication. You can configure it using a `clouds.yaml` file or environment variables.

### Using clouds.yaml

Create a `clouds.yaml` file in your current directory, `~/.config/openstack/`, or `/etc/openstack/`.

See [clouds.yaml.example](clouds.yaml.example) for a template.

### Using Environment Variables

You can also source an OpenStack RC file:

```bash
source project-openrc.sh
os-explorer discover --cloud envvars --out graph.json
```

## Usage

### Discovery

Connect to an OpenStack cloud, discover resources, and save the graph to a JSON file.

```bash
os-explorer discover --cloud mycloud --out graph.json
```

Options:
- `--cloud`: Name of the cloud in `clouds.yaml` (or `envvars`).
- `--region`: OpenStack region name (optional).
- `--out`: Output JSON file path (default: `graph.json`).
- `--debug`: Enable debug logging.

### Tree View

Visualize the resource graph in a hierarchical tree view.

```bash
# Discover and view immediately
os-explorer tree --cloud mycloud

# View from a previously saved JSON file (offline mode)
os-explorer tree --file graph.json
```

### Example Output 

```bash
(venv) ➜  os-reources-viewer os-explorer tree --file graph.json 
Project: admin
├── Servers (10)
│   ├── test-cloud-init-01 (dd88201d-c8d1-4208-9b2d-70114c956885) AZ: HN1 ACTIVE
│   │   ├── Flavor: p2.1c_1g, Image: unknown, Key: trangnth-key, Created: 2025-11-05T03:37:14Z
│   │   ├── Volumes:
│   │   │   └── 5b201d9f-8fcd-46eb-81e9-40c6ec1cadd9 (5b201d9f-8fcd-46eb-81e9-40c6ec1cadd9) (13GB, BASIC-HDD1)
│   │   └── Ports:
│   │       └── 2b2db8c6 (2b2db8c6-5c43-4e1a-8e21-794667007ecf) (10.3.252.176)
│   ├── ops-phungna-test (81001afc-e3ee-49f8-8feb-59910face2b3) AZ: HN1 ACTIVE
│   │   ├── Flavor: e4a.6c_4g, Image: unknown, Created: 2025-10-21T09:43:59Z
│   │   ├── Volumes:
│   │   │   └── phungna-volume-test (4e880b9a-3127-4193-b2a9-c3d31a9cb22d) (40GB, ENTERPRISE-HDD1)
│   │   └── Ports:
│   │       └── 3c03fc3f (3c03fc3f-0cd2-4a03-bd8b-1fc360b72ecf) (2405:f980:0:1:f816:3eff:fe2e:f2f9)
│   ├── trangnth-intel-005 (df7d0a75-6360-4f37-a1c8-d4b8e80de806) AZ: HN2 ACTIVE
│   │   ├── Flavor: nix.2c_2g, Image: unknown, Created: 2025-09-08T10:27:07Z
│   │   ├── Volumes:
│   │   │   └── 50bb18df-7003-4680-8bc7-dec14c4a1cd0 (50bb18df-7003-4680-8bc7-dec14c4a1cd0) (10GB, BASIC-HDD1)
│   │   └── Ports:
│   │       └── 9ff3b766 (9ff3b766-2f75-4b3b-b2c6-57ddea3370d8) (10.3.253.203)
│   ├── trangnth-intel-003 (c409120c-a069-421a-a02f-f9d868d98036) AZ: HN2 ERROR
│   │   └── Flavor: nix.2c_2g, Image: unknown, Created: 2025-09-08T10:26:15Z
│   ├── trangnth-intel-004 (7ebf2479-685b-4137-ae54-4bcc5e1d38ec) AZ: HN2 ACTIVE
│   │   ├── Flavor: nix.2c_2g, Image: unknown, Created: 2025-09-08T10:23:35Z
│   │   ├── Volumes:
│   │   │   └── f52bd589-457e-449e-8688-aba4fcbf44f5 (f52bd589-457e-449e-8688-aba4fcbf44f5) (10GB, BASIC-HDD1)
│   │   └── Ports:
│   │       └── d06fdb08 (d06fdb08-ed39-4233-bf4e-43773ad85d42) (10.3.253.166)
│   ├── trangnth-intel-003 (f4dc0481-8f75-46a9-9e7a-923fd827798a) AZ: HN2 ACTIVE
│   │   ├── Flavor: nix.2c_2g, Image: unknown, Created: 2025-09-08T10:23:01Z
│   │   ├── Volumes:
│   │   │   └── 3b1d059b-ebf6-4377-8126-1bcd3f3807d4 (3b1d059b-ebf6-4377-8126-1bcd3f3807d4) (10GB, BASIC-HDD1)
│   │   └── Ports:
│   │       └── d01eb77f (d01eb77f-ab53-4509-9910-7963116492ea) (10.3.253.85)
│   ├── trangnth-intel-002 (b31395a7-08d5-4b30-99db-d29670a24e8f) AZ: HN2 ACTIVE
│   │   ├── Flavor: nix.2c_2g, Image: unknown, Created: 2025-09-08T10:14:08Z
│   │   ├── Volumes:
│   │   │   └── c3ad970f-72f8-4cb2-b3b3-1484eae50fd6 (c3ad970f-72f8-4cb2-b3b3-1484eae50fd6) (10GB, BASIC-HDD1)
│   │   └── Ports:
│   │       └── 8ef47e09 (8ef47e09-0749-43b3-b9fd-6a38fe347504) (10.3.253.216)
│   ├── trangnth-intel-002 (f55f7bde-80f3-4326-b3d1-b6be374c708b) AZ: HN2 ERROR
│   │   └── Flavor: p2.2c_2g, Image: unknown, Created: 2025-09-08T10:13:09Z
│   ├── trangnth-intel-001 (6ce9e445-813d-4763-b4eb-804d710e3930) AZ: HN2 ACTIVE
│   │   ├── Flavor: p2.2c_2g, Image: unknown, Created: 2025-09-08T10:09:19Z
│   │   ├── Volumes:
│   │   │   └── eea78d37-d13b-4304-b577-42a0f17938a7 (eea78d37-d13b-4304-b577-42a0f17938a7) (10GB, BASIC-HDD1)
│   │   └── Ports:
│   │       └── 201b9450 (201b9450-cbb8-4b90-b8ec-7dbe012e543f) (10.3.253.37)
│   └── minhdq-test-new-compute (fdad06ba-ee00-4fac-b3cb-a1d1d74ef066) AZ: HN1 ACTIVE
│       ├── Flavor: 2c_6g_basic, Image: unknown, Key: mykey, Created: 2025-08-30T03:23:07Z
│       ├── Volumes:
│       │   └── minhdq-test (49d15ff8-3d11-474d-855b-b5d7bd695998) (30GB, BASIC-SSD1)
│       └── Ports:
│           └── e59c2842 (e59c2842-7b80-4b0a-94b7-a2579cb4d665) (10.20.1.57)
├── Networks (4)
│   ├── zun-net (25b8b37d-c866-4ee9-aa07-629690366137)
│   │   └── Subnets:
│   │       └── zun-subnet (f580b07a-6c2d-4322-90c4-692029309924) (CIDR: 192.168.74.0/28, GW: 192.168.74.1)
│   ├── manhnd_test_net_001 (343f0879-4af8-4fc6-8432-14dcab1c1bb4)
│   │   └── Subnets:
│   │       └── manhnd_test_net_001 (605b1231-9edc-46d2-9fe9-1b0e0e7409b5) (CIDR: 172.16.1.0/24, GW: 172.16.1.1)
│   ├── VPNass_staging_HN1 (93db3f52-f51c-4082-a55b-70dc336d4f46)
│   │   └── Subnets:
│   │       └── SUB_VPNass_staging_HN1 (239b4288-4940-44f1-b65e-ed113f2941cf) (CIDR: 10.3.250.0/24, GW: 10.3.250.1)
│   └── 30b04c149e7014b445eb8c7b4567769a68c3fdf8482f417ba64b32752d631f96 (b3d898fb-11c1-44e2-ad19-dd202fa832cd)
│       └── Subnets:
│           └── aaa (49d92e3c-0221-4f47-90a2-55f741c5ef53) (CIDR: 192.168.180.0/24, GW: 192.168.180.1)
├── Routers (9)
│   ├── LB_router_external (0d0bad5b-f063-4463-bb4d-c44ce73f8397) ACTIVE
│   ├── trangnth-iwg-1 (3499d5aa-bdb6-4222-b0fa-bb9ef9143579) ACTIVE
│   ├── manila-router (4672879a-86cb-4941-9f6d-f0181a7aa415) ACTIVE
│   ├── trangnth-test-1 (6d3bb44e-a657-4e6f-a4d0-c6179b7ab983) ACTIVE
│   ├── trangnth-test-1 (9c2950b7-03cc-49a7-bdd5-279d32713563) ACTIVE
│   ├── hungn-test (b0b60de8-7edb-4c3d-b74c-d4f4f1cdb48b) ACTIVE
│   ├── trangnth1 (cebe5eb0-0a67-4027-b563-450e5ad8fb5c) ACTIVE
│   ├── trangnth (f8c9b6ee-0189-4e3f-8d90-ad79cb82116c) ACTIVE
│   └── trangnth-test-1 (fb162464-6524-4983-8940-1a3a0bf62ea2) ACTIVE
├── Volumes (Unattached) (66)
│   ├── trangtest-04 (f610cb66-d1ec-4b1a-9b3b-99f7187577f2) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-04 (6005fdca-e6cb-4b22-8d96-fbff11a119ed) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-04 (5c0e250c-ce78-4b66-a938-b52f9bc0e2eb) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-03 (8ec1dbf2-686d-46f6-b89b-4263d25c67de) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-03 (31acbf4e-1d4d-4941-9fc9-206a67e9d84e) (1GB, PREMIUM-SSD1) available
│   ├── lamth (011410aa-ca0b-4e02-a68d-26e9e1989d57) (10GB, BASIC-SSD1) available
│   ├── lamth (9e17638c-0f67-4a41-94a3-47385ca372e7) (10GB, BASIC-SSD1) available
│   ├── trangtest-03 (c0d2ec8f-027e-49fc-ba9b-491f8e62562a) (1GB, PREMIUM-SSD1) available
│   ├── lamth (7cc71072-97c7-4dc3-b3be-4aac91bcab1f) (10GB, BASIC-SSD1) available
│   ├── trangtest-03 (a64e9124-0840-4925-bc46-9aca5263b450) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-02 (5add81ed-af49-4d07-ae95-257e40f0a6d2) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (710a5809-663e-4c3f-bdfb-bf6cf2937a02) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (d03ae6ef-3bb1-4c12-82c6-949dee14c640) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (66474226-6e79-4048-aef1-f78c166dcf3f) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (ab7ce3ee-1304-44e1-acb5-353d91f4cc2b) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (26a5bd8b-fd4c-41ab-8150-826adf717c7c) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (f45aac64-9509-4b1a-80d0-76cfe44a1531) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (0c311844-7e38-47c1-a563-ba9073d83e75) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (c06fe3e1-5e43-4deb-b2f3-8ab38ffecdb0) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (d3e045c8-b642-4cb3-a068-0384e4258032) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (faee1146-82cf-42c6-9cc5-5610172369f9) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (c1fe5c3d-4a36-455e-a3a2-a990e233da3d) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-02 (02ec4ab4-c8ad-4411-83ff-3ac74206617b) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-02 (dfc23850-735b-47a3-b32d-be36cfe5980f) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-01 (21b3540b-7661-4bbf-80d3-de477dcd1885) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-01 (dd8d1e28-4001-4d44-b219-866f7987ea4c) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-01 (f8ccf807-6c52-4a90-b32e-b3147264ffa3) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-01 (bbd8f9d2-5248-4d83-8c66-afcffb10b605) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-01 (4909e939-a92b-449e-8991-a3a8bc55ab66) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-01 (b8685c74-30bb-446b-b05a-41715e69264a) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-01 (90945628-edf6-49bd-8985-f09c8e3b341a) (1GB, PREMIUM-SSD1) available
│   ├── trangtest-01 (06c2c9b3-4b7b-4e84-98ae-a1f4fbad1234) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-01 (e911d29d-0390-4c6d-a502-d27abc21946f) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-01 (ab10165e-ead3-42fd-9f6d-30654901d66e) (1GB, PREMIUM-SSD1) error
│   ├── trangtest-01 (e41a4b62-feac-4df8-b75e-2efa255298b1) (1GB, PREMIUM-SSD1) error
│   ├── ops-manhnd-test-vol (9d237acc-f093-4a97-a3f0-7dc59f283868) (40GB, PREMIUM-HDD1) reserved
│   ├── ubuntu-2vcpu-2gb-1-0d40q_rootdisk (8ea29e8f-790f-43c6-a36d-1dbdfadff541) (40GB, PREMIUM-SSD1) available
│   ├── ubuntu-2vcpu-2gb-1-0xg0r_rootdisk (9b6488ce-6fa2-4fe1-b297-51225d13e28e) (40GB, ENTERPRISE-HDD1) in-use
│   ├── vupn-test-vl (3e2d3bdf-d5ed-4954-8f5a-b0d9987614b6) (20GB, BASIC-HDD1) available
│   ├── 27186652-6404-4080-8f50-76f6ef6723d4 (27186652-6404-4080-8f50-76f6ef6723d4) (20GB, BASIC-HDD1) available
│   ├── vupn-test-25 (bba66cce-51d3-4d46-9f15-a943d3722fdb) (10GB, NVME1) deleting
│   ├── vupn-test-24 (783199d0-6cc0-412a-b23c-66ed9932a67e) (10GB, NVME1) deleting
│   ├── vupn-test-23 (9157c4d7-d15f-4f02-8a5c-f5aecd9d8292) (10GB, NVME1) deleting
│   ├── vupn-test-22 (8466ec75-1a9a-49a5-bb56-e4c2f65983a4) (10GB, NVME1) deleting
│   ├── vupn-test-21 (97f3148d-fc64-4c83-a957-ae2cbbad81b5) (10GB, NVME1) deleting
│   ├── vupn-test-20 (5d420221-65d1-4ada-8b67-66dbde19703c) (10GB, NVME1) deleting
│   ├── vupn-test-19 (a3cb6f58-77bb-4c85-b2b5-8ddca77e1904) (10GB, NVME1) deleting
│   ├── vupn-test-18 (9bd58c11-9ff0-4d6e-9059-3c411917ef36) (10GB, NVME1) deleting
│   ├── vupn-test-17 (8f99f775-258d-4f10-84cb-0690d2ff03b6) (10GB, NVME1) deleting
│   ├── vupn-test-16 (c28e6881-ca09-43d7-bea7-408d071e05c0) (10GB, NVME1) deleting
│   ├── vupn-test-15 (79674ebb-fccb-4108-b148-f7472b6cdddb) (10GB, NVME1) deleting
│   ├── vupn-test-14 (2658ebfc-184c-44f9-8e84-3439ed481678) (10GB, NVME1) deleting
│   ├── vupn-test-13 (96c9b82a-a066-4eea-bb5c-9707c244563b) (10GB, NVME1) deleting
│   ├── vupn-test-12 (43e2bcad-780a-4473-82b4-c9fefc6a027e) (10GB, NVME1) deleting
│   ├── vupn-test-11 (9914bdcc-3928-4edf-86b9-47874cafa778) (10GB, NVME1) deleting
│   ├── vupn-test-10 (831d4b0f-2cbd-494a-a314-7b959c5a92d0) (10GB, NVME1) deleting
│   ├── vupn-test-9 (9caffaf9-2a4d-42a1-895b-278baef78386) (10GB, NVME1) deleting
│   ├── vupn-test-8 (eb2e9a40-e0b8-4a69-ac09-5c3cfe13315c) (10GB, NVME1) deleting
│   ├── vupn-test-7 (e30eda21-1558-4063-acb2-290b869f7ab1) (10GB, NVME1) deleting
│   ├── vupn-test-6 (9d8d44fc-afeb-4ac2-b922-11f548af07e5) (10GB, NVME1) deleting
│   ├── vupn-test-5 (d1c4577d-63ef-4be8-8bcf-cae8a9a381b8) (10GB, NVME1) deleting
│   ├── vupn-test-4 (94b9e710-0c6f-48a8-a0c3-00f093526248) (10GB, NVME1) deleting
│   ├── vupn-test-3 (729cdc69-7c41-4b7c-87ff-ef4bf07d7513) (10GB, NVME1) deleting
│   ├── vupn-test-2 (009a7a96-1fc8-4cbb-9fdc-b9b6fb9485d0) (10GB, NVME1) deleting
│   ├── vupn-test-1 (76a009cd-8319-4186-ab56-f04572450553) (10GB, NVME1) deleting
│   └── trangnth (5e8964bb-7157-4252-beb6-a3677b940fc9) (10GB, NVME1) deleting
└── Security Groups (2)
    ├── trangnth-sec-grp-1 (3b730804-b649-4d06-9275-48cb412f3ba9)
    │   └── Rules:
    │       ├── ingress tcp 22 -> 0.0.0.0/0
    │       ├── egress icmp Any -> 0.0.0.0/0
    │       ├── egress None Any -> Any
    │       ├── egress None Any -> Any
    │       └── ingress icmp Any -> 0.0.0.0/0
    └── default (41f08d3d-57cd-4e1c-a4f3-c53923c03dce)
        └── Rules:
            ├── ingress None Any -> Group: 41f08d3d-57cd-4e1c-a4f3-c53923c03dce
            ├── ingress None Any -> Group: 41f08d3d-57cd-4e1c-a4f3-c53923c03dce
            ├── egress None Any -> Any
            └── egress None Any -> Any
```




### Documentation

- [Graph JSON Schema](docs/graph_schema.md): Details on the output data format.

