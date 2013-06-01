<?php

class Post_model extends CI_Model {

    public function __construct() {
        $this->load->database();
    }

    public function get_post($id = FALSE) {
        if ($id !== FALSE) {
            $query = $this->db->get_where('post', array('id' => $id));
            return $query->row_array();
        }
        $query = $this->db->get('post');
        return $query->result_array();
    }

}

?>
