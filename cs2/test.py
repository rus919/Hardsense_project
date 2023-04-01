import pyMeow as pm
import time

class offset:
    C_BaseEntity = 0x14A2A48
    m_iHealth = 0x31C

def main():
    cs_proc = pm.open_process(processName="cs2.exe")
    cs_client = pm.get_module(cs_proc, "client.dll")["base"]

    while True:
        # Getting entity
        for i in range(1, 64): # 0 local-player 
            entity = pm.r_uint64(cs_proc, cs_client + offset.C_BaseEntity + i * 0x8)
            if entity != 0:
                try:
                    entity_max_health = pm.r_int(cs_proc, entity + 0x318)
                    if entity_max_health == 100:
                        entity_health = pm.r_int(cs_proc, entity + offset.m_iHealth)
                        print(entity_health) 
                except Exception as err:
                    # print(err)
                    continue
        time.sleep(0.3)

if __name__ == '__main__':
    main()
