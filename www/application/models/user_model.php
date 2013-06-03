<?php

class User_model extends CI_Model {

    public function __construct() {
        $this->load->database();
    }

    public function get_user($id = FALSE) {
        if ($id !== FALSE) {
            $query = $this->db->get_where('user', array('id' => $id));
            return $query->row_array();
        }
        $query = $this->db->get('user');
        return $query->result_array();
    }

    public function add_user() {

        $data = array(
            'name' => $this->input->user('name'),
            'password' => $this->input->user('password'),
            'first_name' => $this->input->user('first_name'),
            'last_name' => $this->input->user('last_name'),
            'nickname' => $this->input->user('nickname'),
            'usr_picture' => $this->input->user('usr_picture'),
           
        );

        return $this->db->insert('user', $data);
    }

}

?>
