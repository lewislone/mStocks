#include <linux/module.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/skbuff.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <net/ip.h>
#include <linux/if_arp.h>
#include <net/arp.h>
#include <uapi/linux/netfilter_arp.h>
#include <linux/inet.h>


#include <linux/fs.h>
#include <linux/seq_file.h>
#include <linux/slab.h>
#include <linux/types.h>
#include <linux/proc_fs.h>
#include <asm/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("lewis <lyl@wangsu.com>");
MODULE_DESCRIPTION("a tool send arp replay");

#if  1
#define DEBUGP printk
#else
#define DEBUGP(format, args...) 
#endif

#define ADD 1
#define DEL 0

struct pod_ip{
    __be32  addr;
    struct pod_ip *next;
};

struct pod_ip_head{
    struct pod_ip *next;
    int nu;
    rwlock_t lock;
};

struct pod_ip_head *ws_pod_ip_head = NULL;

struct proc_dir_entry * proc_dir;

static void add_addr(struct pod_ip *ip)
{
    DEBUGP("add %pI4\n", &ip->addr);
    ip->next = ws_pod_ip_head->next;
    ws_pod_ip_head->next = ip;
    ws_pod_ip_head->nu++;
}

static void del_addr(__be32 addr)
{
    int i = 0;
    struct pod_ip *node = NULL;
    struct pod_ip *pre = NULL;

    write_lock_bh(&ws_pod_ip_head->lock);
    node = ws_pod_ip_head->next;
    for(i = 0; i < ws_pod_ip_head->nu; i++){
        if(addr == node->addr){
            DEBUGP("remove %pI4\n", &node->addr);

            if(pre == NULL){
                ws_pod_ip_head->next = node->next;
                kfree(node);
                node = NULL;
            }else{
                pre->next = node->next;
                kfree(node);
                node = NULL;
            } 
            ws_pod_ip_head->nu--;
            break;
        }
        pre = node;
        node = pre->next;
    }
    write_unlock_bh(&ws_pod_ip_head->lock);
}

static void del_node(struct pod_ip *ip)
{
    del_addr(ip->addr);
}

static void remove_ip_list(void)
{
    int i = 0;
    struct pod_ip *node;

	for (i = 0; i < ws_pod_ip_head->nu; i++){
        node = ws_pod_ip_head->next;
        del_node(node);
    }
    kfree(ws_pod_ip_head);
}

static int pod_ipv4_ip_show(struct seq_file *seq, void *v)
{
    int i = 0;
    int ret = -1;
    struct pod_ip *node;
    
    if(ws_pod_ip_head == NULL){
        printk("ws_pod_ip_head uninit\n");
        return ret;
    }
    node = ws_pod_ip_head->next;
	for (i = 0; i < ws_pod_ip_head->nu; i++){
		seq_printf(seq, "%pI4\n", &node->addr);
        node = node->next;
    }

    return 0;
}

static int pod_ipv4_ip_open(struct inode *inode, struct file *file)
{
    return single_open(file, pod_ipv4_ip_show, inode->i_private);
}

static ssize_t pod_ip_write(struct file *file, const char __user *buf,
			    size_t count, loff_t *ppos)
{
    int i = 0;
    int add = 0;
    int ret = -1;
    char data[32];
    __be32 addr = 0;
    struct pod_ip *localip;
    struct pod_ip *node;

    if (count < 8) {//+0.0.0.0
       printk("wrong command format\n");
        goto out;
    }

    if (copy_from_user(data, buf, count)) {
        printk("failed copy_from_user\n");
        goto out;
    }
    
    switch(data[0]){
    case '+':
        add = 1;
    case '-':
        addr = in_aton(&data[1]);
        break;
    default:
	printk("wrong command format\n");
        goto out;
    }
    if(addr != 0){
        //TODO:verify ip addr

        if(add == 1){
            node = ws_pod_ip_head->next;
	    for(i = 0; i < ws_pod_ip_head->nu; i++){
                if(addr == node->addr){
                    printk("%pI4 exist\n", &addr);
                    ret = count;
                    goto out;
                }
                node = node->next;
            }

            //add addr to ws local list
            localip = kmalloc(sizeof(struct pod_ip), GFP_KERNEL);
            if(localip == NULL){
                printk("kmalloc pod_ip failed\n");
                goto out;
            }
	        memset(localip, 0, sizeof(struct pod_ip));
            localip->addr = addr;
            add_addr(localip);
        }else{
            del_addr(addr);
        }
        return count;
    }

out:
    return ret;

}

static const struct file_operations pod_ipv4_ip_fops = {
	.owner	 = THIS_MODULE,
	.open	 = pod_ipv4_ip_open,
	.read	 = seq_read,
	.write	 = pod_ip_write,
	.llseek = seq_lseek,
	.release = single_release,
};

static int init_ip_list(void)
{
    int ret = 0;

    ws_pod_ip_head = kmalloc(sizeof(struct pod_ip_head), GFP_KERNEL);
    if(ws_pod_ip_head == NULL){
        printk("init ws_pod_ip_head failed\n");
        ret = -1;
    }else{
        ws_pod_ip_head->nu = 0;
		rwlock_init(&ws_pod_ip_head->lock);
    }

    return ret;
}


static char mac_buf[35] = {0};
module_param_string(mac_buf, mac_buf, sizeof(mac_buf), 0644);
MODULE_PARM_DESC(mac_buf, "mac addr in arp replay");

static int
replay_arp(struct sk_buff *skb, const struct net_device *in)
{
	unsigned char mac[ETH_ALEN];
        const __be32 *siptr, *diptr;
        __be32 _sip, _dip;
        const struct arphdr *ap;
        struct arphdr _ah;
        const unsigned char *shp;
        unsigned char _sha[ETH_ALEN];
	int i = 0;
	int found = 0;
	struct pod_ip *node;

	sscanf(mac_buf, "%02x:%02x:%02x:%02x:%02x:%02x", &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5]);

        ap = skb_header_pointer(skb, 0, sizeof(_ah), &_ah);
        if (ap == NULL)
                return -1;

        if (ap->ar_op != htons(ARPOP_REQUEST) ||
            ap->ar_hln != ETH_ALEN ||
            ap->ar_pro != htons(ETH_P_IP) ||
            ap->ar_pln != 4)
                return -1;

        shp = skb_header_pointer(skb, sizeof(_ah), ETH_ALEN, &_sha);
        if (shp == NULL)
                return -1;

        siptr = skb_header_pointer(skb, sizeof(_ah) + ETH_ALEN,
                                   sizeof(_sip), &_sip);
        if (siptr == NULL)
                return -1;

        diptr = skb_header_pointer(skb,
                                   sizeof(_ah) + 2 * ETH_ALEN + sizeof(_sip),
                                   sizeof(_dip), &_dip);
        if (diptr == NULL)
                return -1;

	printk("%u; dst:%pI4:%u; src:%pI4:%u\n", in_aton("172.16.144.133"), diptr,*diptr, siptr,*siptr);
        node = ws_pod_ip_head->next;
	for(i = 0; i < ws_pod_ip_head->nu; i++){
		if(*diptr == node->addr){
			found = 1;
			break;
		}
                node = node->next;
	}
	if (found == 0)
                return -1;

	//mac[0] = 0x16; 
	//mac[1] = 0x7f; 
	//mac[2] = 0x29; 
	//mac[3] = 0xd6; 
	//mac[4] = 0x8f; 
	//mac[5] = 0x16; 

        arp_send(ARPOP_REPLY, ETH_P_ARP, *siptr, skb->dev, *diptr, shp, mac, shp);

        return 0;
}


static unsigned int
arp_reply_hook(const struct nf_hook_ops *ops, struct sk_buff *skb,
                    const struct net_device *in, const struct net_device *out,
                    const struct nf_hook_state *state)
{
   int ret = 0;
   printk(" in arp_reply_hook!!!\n");
   if(skb){
       ret = replay_arp(skb, in);
       if(ret < 0){
            printk("replay arp failed!!!\n");
   	    return NF_ACCEPT;
       }
   }
   return NF_STOLEN;
   //return NF_ACCEPT;
}

static struct nf_hook_ops arp_reply = {
    .hook = arp_reply_hook,
    .owner = THIS_MODULE,
    .pf = NFPROTO_ARP,
    .hooknum = NF_ARP_IN,
    .priority = NF_IP_PRI_FILTER-1,
};


static int __init arp_reply_init(void)
{
	int ret = 0;
	ret = nf_register_hook(&arp_reply);
	if(ret < 0){
		printk("register_hook failed!!!!\n");
		goto out;
	}

	if(init_ip_list()){
	    printk("init failed!\n");
	    ret =  -1;
	    goto out2;
	}

	proc_dir = proc_mkdir("arp_replay", NULL);
	if (!proc_dir) {
	    ret = -1;
	    goto out2;
	} 

	if (!proc_create("pod_ip_list", S_IRUGO|S_IWUGO, proc_dir, &pod_ipv4_ip_fops)){
	    printk("crete proc failed\n");
	    remove_ip_list();
	    ret = -1;
	    goto out2;
	}
out:
	return ret;
out2:
	nf_unregister_hook(&arp_reply);
	return ret;

}

static void __exit arp_reply_exit(void)
{
	nf_unregister_hook(&arp_reply);
	remove_ip_list();
	remove_proc_entry("pod_ip_list", proc_dir);
	remove_proc_entry("arp_replay", NULL);
}

module_init(arp_reply_init);
module_exit(arp_reply_exit);
MODULE_LICENSE("GPL");
