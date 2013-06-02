<?php

class Post extends CI_Controller {

    public function __construct() {
        parent::__construct();
        $this->load->model('post_model');
        $this->load->model('tag_model');
    }

    public function index() {
        $data['post'] = $this->post_model->get_post();
        $data['title'] = 'All posts';
        $this->load->view('templates/header', $data);
        $this->load->view('post/index', $data);
        $this->load->view('templates/footer');
    }

    public function view($id) {

        $data['item'] = $this->post_model->get_post($id);
        $data['tags'] = $this->tag_model->get_all_tags_to_post($id);

        if (empty($data['item'])) {
            show_404();
        }

        $data['title'] = $data['item']['title'];

        $this->load->view('templates/header', $data);
        $this->load->view('post/view', $data);
        $this->load->view('templates/footer');
    }

    public function add() {
        $this->load->helper('form');
        $this->load->library('form_validation');

        $data['title'] = 'Add new post';

        $this->form_validation->set_rules('title', 'Title', 'required');
        $this->form_validation->set_rules('text', 'text', 'required');

        if ($this->form_validation->run() === FALSE) {
            $this->load->view('templates/header', $data);
            $this->load->view('post/add');
            $this->load->view('templates/footer');
        } else {
            $this->post_model->set_post();
            $this->load->view('info');
        }
    }

}
