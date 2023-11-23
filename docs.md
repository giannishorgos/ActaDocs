# Acta Docs
Welcome to ***Acta Tasks and Issues*** documentation. This version is still in it's initial form. Stay tuned to see this playground transform in a well-structured guide!

## Table of Contents
- [Database and Periodic Inform Distribution](#database-and-periodic-inform)
- [AXESS - Multi Tenancy](#axess---multi-tenancy)
# Database and periodic inform

Η mysql τρέχει στον DB01/DB02 (ip1, ip2), sto chroot /opt/mysql5.7

The script responsible for the distribution of Periodic Informs (PI) is as follows:

```python
from random import random

def pit_uniform_distribution():
  pii = 21600 # Periodic Time Interval That CPE communicates. ex: 21600 s = 6 h every 6 hours
  pii_start_time_seconds = 0 # shift the start time
  pii_time_window_seconds = 6 * pii # PII is 6 hours or 21600 seconds
  random_seconds = int(random() * (pii_time_window_seconds + 1)) # random numbers in order to achive uniform distribution.
                                                                 # MAX value: 6 * (pii + 1), MIN value: 0
  start_time = pii_start_time_seconds + random_seconds

  hours = '%02d' % ((start_time // pii % 24) + 4)
  minutes = '%02d' % (start_time // 60 % 60)
  seconds = '%02d' % (start_time % 60)
  periodic_inform_time = ({'hours':hours}, {'minute' : minutes}, {'seconds':seconds})
  return periodic_inform_time
```
## AXESS - Multi Tenancy

#### Step 1: Define the tenancy matrix
Let's say we have two tenants with names amazing and fantastic, respectively.
We should define the relation of these two tenants with the Administator of the platform as well as the relation between the tenanants.
In this example, we assume that the 2 tenants are 1-level below the Admin and in the same level. So graphically we have the following:

```
ADMIN:      *
           / \
Tenants: (1) (2)
```
*(1): amazing, (2): fantastic*

We define this relation schema by creating a python script anywhere in the ACS. A good practice is to create a folder `logic/` and place the `tenancy-graph.py` script inside:
```python
graph_dict = {
    'ADMIN': ['amazing', 'fantastic']
}

container.Tenancy.store_graph_dict(graph_dict) # store the defined Tenants relations

print(container.Tenancy.get_graph().as_dict()) # print the stored graph

return printed # display what we print
```
Once we run the script by clicking the 'Run' button, the graph is stored in the ACS Multi-Tenancy configuration.


#### Step 2: Assign users to tenant via dynamic hook
Now that we have declared the tenants, we created 2 users `amazing_user1` and `fantastic_user2` and we want to assign them to the corresponding tenant.
To do this, we need to modify the script `tenant_accounts/lookup_successful_hook.py` that is called after the user is loaded from the Database, i.e., after login.
Here, we are following a **naming convention** from users. Specifically, each username should following this rule: `<tenant_name>_<username>`:

Script Parameters: `uid, pwd, request, db_props, log`
```python
try:
    tenant, _ = uid.split('_', 1)
    if tenant in ['amazing', 'fantastic']:
        db_props['tenant'] = tenant
except:
    pass

# Returning True means we update the tenant info in the DB for the specific user
# Returning False means that ACS will handle this as "User not found"
return True
```
Now if we logout and login as -let's say- `amazing_user1` we will see that we can manage only the CPEs that are assigned to **amazing**.

#### Step 3: Assign CPEs to tenant via policy
The next step is to set CPEs population to tenant so the users of each tenant to manage their CPEs.
We will creat a script that check the CPE id and if it starts with ***ZZ*** will set the CPE to tenant **fantastic**, otherwise, if it starts with ***XX*** will set the CPE to **amazing**.

The script will be used by a policy that runs on **BOOTSTRAP** events so it should be place under **live/CPEManager/Scenarios/policies/** directory.

Script Parameters: `initargs, run_scenario, cpe`
```python
if cpe.cpeid.startswith("ZZ"):
    cpe.set('tenant', 'fantastic') # set is a build-in method of cpe object

if cpe.cpeid.startswith("XX"):
    cpe.set('tenant', 'amazing')

return "Done"
```
After we implement the bussiness logic of our script, we simply create a policy that runs on **BOOTSTRAP** events and executes the above script. This will result to a split in CPEs population based on tenants. The users that belong to a tenant can see only the CPEs within its tenant.

#### Final Conclusions: 
The multi-tenancy allows multiple companies/customers to work in the same ACS. While the **resources** of the application such as Servers, Databases etc., are **shared** among all tenants, **the management** of CPEs, users, policies, campaings, data export etc., is totally **independent and isolated** between tenants. Tenants on the same level cannot interact with anything outside their scope.
