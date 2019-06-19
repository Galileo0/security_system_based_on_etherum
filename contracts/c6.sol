pragma solidity ^0.4.5;
//import "StringUtils.sol";
//import "github.com/ethereum/dapp-bin/blob/master/library/stringUtils.sol";
contract resident_visiting
{
    
     struct resdent
     {
        string res_add;
        string pk;
        string email;
     }
    
    struct visitor
    {
        string name;
        string phone_num;
        string car_num;
        uint qr_code_expiration;
        string token;
        address resident_address;
        string email;
    }
    
    struct tracking
    {
        string name;
        string phone_num;
        string car_num;
        string location;
        string time;
        address locater;
        address resident;
    }
    
    struct worker
    {
        string name;
        string car_num;
        string qr_code_expiration;
        string token;
        string email;
        string job;
        string days_access;
    }
    
    struct worker_res
    {
        string token;
        address resident_address;
    }
    
    struct blacklist
    {
        string email;
        uint statu;
        string key;
    }
    
    mapping (uint => visitor) public visitor_struct;
    mapping (uint => tracking) public sec_tracking;
    mapping (uint => worker) public worker_struct;
    mapping (uint => worker_res) public worker_res_str;
    mapping (uint => resdent) public resdent_struct;
    mapping (uint => blacklist) public blacklist_struct;
    
    
    
    uint visitor_struct_count;
    uint cars_tracking;
    uint vis_worker;
    uint res_worker;
    uint resdent_count;
    uint blacklist_count;
    
    function revoke_res(string _email,uint val) public returns(int)
    {
        for (uint i = 1; i <= resdent_count;i++)
        {
            resdent temp = resdent_struct[i];
            string temp_email = temp.email;
            if(stringsEqual(temp_email,_email))
            {
                for (uint ii = 1; ii<blacklist_count;ii++)
                {
                    blacklist bl_temp = blacklist_struct[ii];
                    string bl_email = bl_temp.email;
                    if(stringsEqual(bl_email,_email))
                    {
                        bl_temp.statu = val;
                        return 1;
                    }
                }
                
                blacklist_count++;
                blacklist_struct[blacklist_count] = blacklist(_email,val,temp.pk);
                return 1;
            }
        }
        return 0;
    }
    
    function revoke_visitor(string _email,uint val) public returns(int)
    {
        for (uint j = 1; j <= visitor_struct_count;j++)
        {
            visitor temp2 = visitor_struct[j];
            string temp_email2 = temp2.email;
            if(stringsEqual(temp_email2,_email))
            {
                for (uint jj = 1; jj<blacklist_count;jj++)
                {
                    blacklist bl_temp2 = blacklist_struct[jj];
                    string bl_email2 = bl_temp2.email;
                    if(stringsEqual(bl_email2,_email))
                    {
                        bl_temp2.statu = val;
                        return 1;
                    }
                }
                
                blacklist_count++;
                blacklist_struct[blacklist_count] = blacklist(_email,val,temp2.token);
                return 1;
            }
        }
        return 0;
    }
    
    function revoke_worker(string _email,uint val) public returns (int)
    {
        for (uint e = 1; e <= vis_worker;e++)
        {
            worker temp3 = worker_struct[e];
            string temp_email3 = temp3.email;
            if(stringsEqual(temp_email3,_email))
            {
                for (uint ee = 1; ee<blacklist_count;ee++)
                {
                    blacklist bl_temp3 = blacklist_struct[ee];
                    string bl_email3 = bl_temp3.email;
                    if(stringsEqual(bl_email3,_email))
                    {
                        bl_temp3.statu = val;
                        return 1;
                    }
                }
                
                blacklist_count++;
                blacklist_struct[blacklist_count] = blacklist(_email,val,temp3.token);
                return 1;
            }
        }
        return 0;
    }
    
    function check_revoke(string _key) public returns(uint)
    {
        for (uint e = 1; e <= blacklist_count;e++)
        {
            blacklist temp = blacklist_struct[e];
            if(stringsEqual(temp.key,_key))
            {
                return temp.statu;
            }
        }
        
        return 0;
    }
    
    function add_resdent(string _email, string _pk,string _res_add) public
    {
        resdent_count++;
        resdent_struct[resdent_count] = resdent(_res_add,_pk,_email);
        
    }
    
    function init_worker(string _token , string _qr_code_expire,string _email,string _days_access,string _name,string car_num,string _job) public
    {
        vis_worker++;
        res_worker++;
        worker_struct[vis_worker] = worker(_name,car_num,_qr_code_expire,_token,_email,_job,_days_access);
        worker_res_str[res_worker] = worker_res(_token,msg.sender); 
    }    
    
    function init_visiting(string _token , uint _qr_code_expire,string _email,string _phone_num,string _name,string car_num) public
    {
        visitor_struct_count++;
        address _res_address = msg.sender;
        visitor_struct[visitor_struct_count] = visitor(_name,_phone_num,car_num,_qr_code_expire,_token,_res_address,_email);
        
    }
    
    function auth_resdent(string _pk) public returns(int)
    {
        for (uint i = 1; i <= resdent_count;i++)
        {
            resdent temp = resdent_struct[i];
            string temp_pk = temp.pk;
            if(stringsEqual(temp_pk,_pk))
            {
                return 1;
            }
        }
        
        return 0;
    }
    
    
    
    function auth(string _token) public returns(int)
    {
         for (uint i = 1; i <= visitor_struct_count;i++)
         {
            visitor temp = visitor_struct[i];
            string temp_token = temp.token;
            
            if(stringsEqual(temp_token,_token))
            {
                if(temp.qr_code_expiration != 0)
                {
                    visitor_struct[i].qr_code_expiration --;
                    return 1;
                }else
                {
                    return 0;
                }
            }
            
         }
         
         return 0;
    }
    
    function auth_worker(string _token) public returns(string,string)
    {
        for (uint i = 1; i <= vis_worker;i++)
         {
            worker temp = worker_struct[i];
            string temp_token = temp.token;
            
            if(stringsEqual(temp_token,_token))
            {
                return(temp.qr_code_expiration,temp.days_access);
            }
         }
         
         return ("NULL","NULL");
    }
    
    function edit_worker_access(string _email,string _duration,string _days) public returns(int)
    {
        for (uint i = 1; i <= vis_worker;i++)
         {
            worker temp = worker_struct[i];
            string temp_email = temp.email;
            
            if(stringsEqual(temp_email,_email))
            {
                worker_struct[i].qr_code_expiration = _duration;
                worker_struct[i].days_access = _days;
                return 1;
            }
         }
         
         return 0;
        
    }
    
    function auth_out(string _token) public returns(int)
    {
         for (uint i = 1; i <= visitor_struct_count;i++)
         {
            visitor temp = visitor_struct[i];
            string temp_token = temp.token;
            
            if(stringsEqual(temp_token,_token))
            {
                    return 1;
            }
            
         }
         
         return 0;
    }
    
    function auth_out_worker(string _token) public returns(int)
    {
         for (uint i = 1; i <= vis_worker;i++)
         {
            worker temp = worker_struct[i];
            string temp_token = temp.token;
            
            if(stringsEqual(temp_token,_token))
            {
                return 1;
            }
         }
         
         return 0;
    }
    
    
    function track(string _car_num,string location , string time) public returns(int) // tracking function
    {
        // step 1 verfy car with visitor struct
        for(uint i = 1; i<= visitor_struct_count; i++)
        {
            visitor temp = visitor_struct[i]; // get visitor complete_data
            if(stringsEqual(temp.car_num,_car_num))
            {                                           // found | log
                cars_tracking++;
                string _name = temp.name;
                string _phone = temp.phone_num;
                address _locater_device = msg.sender;
                address _res_address = temp.resident_address;
                sec_tracking[cars_tracking] = tracking(_name,_phone,_car_num,location,time,_locater_device,_res_address);
                return 1;
            }
            
        }
        return 0;
    }
    
    
    
     function track_worker(string _car_num,string location , string time) public returns (int)
    {
        
        for(uint j = 1; j<= vis_worker; j++)
        {
            worker temp_w = worker_struct[j];
            worker_res temp2_w = worker_res_str[j];
            if(stringsEqual(temp_w.car_num , _car_num))
            {
                cars_tracking++;
                string _name_w = temp_w.name;
                address _locater_device_w = msg.sender;
                address _res_address_w = temp2_w.resident_address;
                sec_tracking[cars_tracking] = tracking(_name_w,'000000',_car_num,location,time,_locater_device_w,_res_address_w);
                return 1;
            }
        }
        return 0;
    }
    
    function track_in_out(string _token,string _location,string _time) public returns (int)
    {
        for(uint i = 1; i<= visitor_struct_count; i++)
        {
            visitor temp = visitor_struct[i]; // get visitor complete_data
            if(stringsEqual(temp.token,_token))
            {                                           // found | log
                cars_tracking++;
                string _name = temp.name;
                string _phone = temp.phone_num;
                address _locater_device = msg.sender;
                address _res_address = temp.resident_address;
                sec_tracking[cars_tracking] = tracking(_name,_phone,'_car_num',_location,_time,_locater_device,_res_address);
                return 1;
            }
            
        }
        
        
        return 0;
        
    }
    
    function track_in_out_worker(string _token,string _location,string _time) public returns (int)
    {
        for(uint j = 1; j<= vis_worker; j++)
        {
            worker temp_w = worker_struct[j];
            worker_res temp2_w = worker_res_str[j];
            if(stringsEqual(temp_w.token,_token))
            {
                cars_tracking++;
                string _name_w = temp_w.name;
                address _locater_device_w = msg.sender;
                address _res_address_w = temp2_w.resident_address;
                sec_tracking[cars_tracking] = tracking(_name_w,'worker','_car_num',_location,_time,_locater_device_w,_res_address_w);                
                return 1;
            }
        }
    }
    
    
    
     // Security Building Functions
    
    function get_visitor_count() public returns (uint)
    {
        return visitor_struct_count;
    }
    
    
    function get_track_logs_count() public returns (uint)
    {
        return cars_tracking;
    }
    
    
    
    function get_workers_count() public returns (uint)
    {
        return vis_worker;
    }
    
    
    function get_visitor(uint _index) public returns(string,string,string,uint,string,address,string)
    {
        visitor temp = visitor_struct[_index];
        return (temp.name,temp.phone_num,temp.car_num,temp.qr_code_expiration,temp.token,temp.resident_address,temp.email);
    }
    
    function get_worker(uint _index) public returns(string,string,string,string,string,address,string)
    {
        worker temp1 = worker_struct[_index];
        worker_res temp2 = worker_res_str[_index];
        return (temp1.name,'worker_phone',temp1.car_num,temp1.qr_code_expiration,temp1.token,temp2.resident_address,temp1.email);
    }
    
     function get_track(uint _index) public returns(string,string,string,string,string,address,address)
    {
        tracking temp = sec_tracking[_index];
        return (temp.name,temp.phone_num,temp.car_num,temp.location,temp.time,temp.locater,temp.resident);
    }
    
    //--------------------------
    
    
    function stringsEqual(string storage _a, string memory _b) internal returns (bool) {
		bytes storage a = bytes(_a);
		bytes memory b = bytes(_b);
		if (a.length != b.length)
			return false;
		// @todo unroll this loop
		for (uint i = 0; i < a.length; i++)
			if (a[i] != b[i])
				return false;
		return true;
	}
}