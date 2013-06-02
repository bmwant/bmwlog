<?php

class Tag_model extends CI_Model {

    public function __construct() {
        $this->load->database();
    }

    public function get_all_tags_to_post($post_id) {
        $all_tags_id = $this->db->get_where('tag_to_post', array('post_id' => $post_id))->result_array();
        $array = Array();
        foreach ($all_tags_id as $tag) {
            $query = $this->db->get_where('tag', array('id' => $tag['tag_id']))->row_array();
            $array[] = $query['text'];
        }
        return $array;
    }

    public function add_tag() {

        $data = array(
            'title' => $this->input->post('title'),
            'text' => $this->input->post('text')
        );

        return $this->db->insert('post', $data);
    }

}

?>
