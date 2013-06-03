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

        $password = $this->encrypt_password($this->input->post('password'));
        $data = array(
            'email' => $this->input->post('email'),
            'password' => $password,
            'first_name' => $this->input->post('fname'),
            'last_name' => $this->input->post('lname'),
            'nickname' => $this->input->post('nickname'),
                //'usr_picture' => $this->input->post('usr_picture'),  
        );

        return $this->db->insert('user', $data);
    }

    private function encrypt_password($password) {
        return sha1(md5($password) . $this->config->item('encryption_key'));
    }

    public function validate() {
        $email = $this->input->post('email');
        $password = $this->encrypt_password($this->input->post('password'));
        $query = $this->db->get_where('user', array('email' => $email, 'password' => $password));
        $this->load->view('info', array('data' => $query->num_rows()));
        return TRUE;
    }

    private function set_session($query) {
        $row = $query->result_array();
        $data = array(
            'userid' => $row['id'],
            'nickname' => $row['nickname'],
            'validated' => true
        );
        $this->session->set_userdata($data);
    }

}

?>
